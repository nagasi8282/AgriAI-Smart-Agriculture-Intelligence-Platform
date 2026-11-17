"""
AgriAI Medallion Data Engineering - Transformation & Warehouse Service
Manages Bronze -> Silver (Cleaning & Deduplication) -> Gold (Star Schema Marts) transformations.
Supports SQLite (local dev/testing) and PostgreSQL (production).
"""

import hashlib
import logging
from datetime import datetime, date, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple
import pandas as pd
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import sessionmaker, Session

from backend.config.settings import settings
from backend.models.medallion_models import (
    Base,
    StagingCropProduction,
    StagingMandiPrice,
    StagingWeather,
    StagingSoil,
    DimDate,
    DimLocation,
    DimCrop,
    DimMarket,
    FactCropProduction,
    FactMandiPrice,
    FactWeather,
    FactSoil,
)
from storage.local_storage import local_storage

logger = logging.getLogger("agriai.medallion")


class MedallionWarehouseService:
    """Orchestrates transformation from raw Bronze lake to Gold dimensional marts."""

    DISTRICT_CANONICAL_MAP = {
        "guntur": "Guntur",
        "krishna": "Krishna",
        "kurnool": "Kurnool",
        "anantapur": "Anantapur",
        "east godavari": "East Godavari",
        "e. godavari": "East Godavari",
        "e godavari": "East Godavari",
        "chittoor": "Chittoor",
        "prakasam": "Prakasam",
        "west godavari": "West Godavari",
        "w. godavari": "West Godavari",
        "visakhapatnam": "Visakhapatnam",
        "vizag": "Visakhapatnam",
        "nellore": "Nellore",
        "spsr nellore": "Nellore",
        "ysr kadapa": "YSR Kadapa",
        "kadapa": "YSR Kadapa",
        "cuddapah": "YSR Kadapa",
        "srikakulam": "Srikakulam",
        "vizianagaram": "Vizianagaram",
    }

    CROP_CANONICAL_MAP = {
        "paddy": "Paddy (Rice)",
        "rice": "Paddy (Rice)",
        "dhan": "Paddy (Rice)",
        "paddy (rice)": "Paddy (Rice)",
        "cotton": "Cotton",
        "chillies": "Chillies",
        "chilli": "Chillies",
        "red chilli": "Chillies",
        "groundnut": "Groundnut",
        "peanut": "Groundnut",
        "maize": "Maize",
        "corn": "Maize",
        "bengal gram": "Bengal Gram",
        "chickpea": "Bengal Gram",
        "gram": "Bengal Gram",
        "sugarcane": "Sugarcane",
    }

    AGRO_ZONES = {
        "Guntur": "Krishna-Godavari Coastal Zone",
        "Krishna": "Krishna-Godavari Coastal Zone",
        "East Godavari": "North Coastal Delta Zone",
        "West Godavari": "Krishna-Godavari Coastal Zone",
        "Visakhapatnam": "North Coastal Hill Zone",
        "Srikakulam": "North Coastal Zone",
        "Vizianagaram": "North Coastal Zone",
        "Prakasam": "Southern Coastal Zone",
        "Nellore": "Southern Coastal Zone",
        "Kurnool": "Scarce Rainfall Rayalaseema Zone",
        "Anantapur": "Scarce Rainfall Rayalaseema Zone",
        "YSR Kadapa": "Southern Dry Rayalaseema Zone",
        "Chittoor": "Southern Dry Zone",
    }

    def __init__(self, db_url: Optional[str] = None):
        # Default to local SQLite database for zero-config testing if PostgreSQL is unavailable
        if not db_url:
            db_path = Path(settings.DATA_DIR) / "agriai_warehouse.db"
            db_url = f"sqlite:///{db_path}"

        self.engine = create_engine(db_url, echo=False)
        self.SessionFactory = sessionmaker(bind=self.engine)
        self._initialize_schema()

    def _initialize_schema(self) -> None:
        """Create tables for Silver and Gold layers if they do not exist."""
        Base.metadata.create_all(self.engine)

    def get_session(self) -> Session:
        return self.SessionFactory()

    @classmethod
    def standardize_district(cls, raw_district: str) -> str:
        key = str(raw_district).strip().lower()
        return cls.DISTRICT_CANONICAL_MAP.get(key, raw_district.strip().title())

    @classmethod
    def standardize_crop(cls, raw_crop: str) -> str:
        key = str(raw_crop).strip().lower()
        return cls.CROP_CANONICAL_MAP.get(key, raw_crop.strip().title())

    # ==========================================================================
    # BRONZE -> SILVER TRANSFORMATION (Cleaning, Standardization, Deduplication)
    # ==========================================================================

    def transform_bronze_to_silver(self) -> Dict[str, int]:
        """Process raw/sample data into Silver cleaned staging tables."""
        session = self.get_session()
        counts = {"crops": 0, "mandi": 0, "weather": 0, "soil": 0}

        try:
            # 1. Transform Crop Production
            crop_df = local_storage.load_sample_dataset("crop_production")
            for _, r in crop_df.iterrows():
                std_dist = self.standardize_district(r["district_name"])
                std_crop = self.standardize_crop(r["crop"])
                chk = hashlib.sha256(f"{std_dist}_{r['crop_year']}_{r['season']}_{std_crop}".encode()).hexdigest()

                if not session.query(StagingCropProduction).filter_by(_checksum=chk).first():
                    stg = StagingCropProduction(
                        state=r.get("state_name", "Andhra Pradesh"),
                        district=std_dist,
                        crop_year=int(r["crop_year"]),
                        season=str(r["season"]),
                        crop=std_crop,
                        area_hectares=float(r["area_hectares"]),
                        production_tonnes=float(r["production_tonnes"]),
                        yield_quintal_per_ha=float(r["yield_quintal_per_ha"]),
                        _checksum=chk,
                    )
                    session.add(stg)
                    counts["crops"] += 1

            # 2. Transform Mandi Prices
            mandi_df = local_storage.load_sample_dataset("mandi_prices")
            for _, r in mandi_df.iterrows():
                std_dist = self.standardize_district(r["district"])
                std_crop = self.standardize_crop(r["commodity"])
                arr_date = datetime.strptime(str(r["arrival_date"]), "%Y-%m-%d").date()
                chk = hashlib.sha256(f"{std_dist}_{r['market']}_{std_crop}_{arr_date}".encode()).hexdigest()

                if not session.query(StagingMandiPrice).filter_by(_checksum=chk).first():
                    stg = StagingMandiPrice(
                        state=r.get("state", "Andhra Pradesh"),
                        district=std_dist,
                        market=str(r["market"]),
                        commodity=std_crop,
                        variety=str(r.get("variety", "Standard")),
                        arrival_date=arr_date,
                        min_price_inr=float(r["min_price_inr"]),
                        max_price_inr=float(r["max_price_inr"]),
                        modal_price_inr=float(r["modal_price_inr"]),
                        arrival_tonnes=float(r.get("arrival_tonnes", 0.0)),
                        _checksum=chk,
                    )
                    session.add(stg)
                    counts["mandi"] += 1

            # 3. Transform Weather
            weather_df = local_storage.load_sample_dataset("weather")
            for _, r in weather_df.iterrows():
                std_dist = self.standardize_district(r["district"])
                obs_date = datetime.strptime(str(r["date"]), "%Y-%m-%d").date()
                chk = hashlib.sha256(f"{std_dist}_{obs_date}".encode()).hexdigest()

                if not session.query(StagingWeather).filter_by(_checksum=chk).first():
                    stg = StagingWeather(
                        district=std_dist,
                        observation_date=obs_date,
                        temp_max_c=float(r["temp_max_c"]),
                        temp_min_c=float(r["temp_min_c"]),
                        temp_mean_c=float(r["temp_mean_c"]),
                        rainfall_mm=float(r["rainfall_mm"]),
                        relative_humidity_pct=float(r["relative_humidity_pct"]),
                        wind_speed_kmh=float(r["wind_speed_kmh"]),
                        is_forecast=bool(r.get("is_forecast", False)),
                        condition=str(r.get("condition", "Normal")),
                        _checksum=chk,
                    )
                    session.add(stg)
                    counts["weather"] += 1

            # 4. Transform Soil
            soil_df = local_storage.load_sample_dataset("soil_health")
            for _, r in soil_df.iterrows():
                std_dist = self.standardize_district(r["district"])
                chk = hashlib.sha256(f"{std_dist}_soil".encode()).hexdigest()

                if not session.query(StagingSoil).filter_by(_checksum=chk).first():
                    stg = StagingSoil(
                        district=std_dist,
                        soil_type=str(r["soil_type"]),
                        available_nitrogen_kg_ha=float(r["available_nitrogen_kg_ha"]),
                        available_phosphorus_kg_ha=float(r["available_phosphorus_kg_ha"]),
                        available_potassium_kg_ha=float(r["available_potassium_kg_ha"]),
                        soil_ph=float(r["soil_ph"]),
                        organic_carbon_pct=float(r["organic_carbon_pct"]),
                        electrical_conductivity_dsm=float(r["electrical_conductivity_dsm"]),
                        nitrogen_category=str(r.get("nitrogen_category", "Medium")),
                        phosphorus_category=str(r.get("phosphorus_category", "Medium")),
                        potassium_category=str(r.get("potassium_category", "Medium")),
                        _checksum=chk,
                    )
                    session.add(stg)
                    counts["soil"] += 1

            session.commit()
            return counts
        except Exception as e:
            session.rollback()
            logger.error(f"Error during Bronze -> Silver transformation: {e}")
            raise e
        finally:
            session.close()

    # ==========================================================================
    # SILVER -> GOLD TRANSFORMATION (Dimensional Star Schema Loading)
    # ==========================================================================

    def transform_silver_to_gold(self) -> Dict[str, int]:
        """Populate Gold dimension and fact tables from Silver conformed tables."""
        session = self.get_session()
        counts = {"dim_location": 0, "dim_crop": 0, "dim_market": 0, "dim_date": 0, "facts": 0}

        try:
            # 1. Populate DimLocation
            districts = session.query(StagingCropProduction.district).distinct().all()
            for (dist,) in districts:
                if not session.query(DimLocation).filter_by(district=dist).first():
                    dim_loc = DimLocation(
                        state="Andhra Pradesh",
                        district=dist,
                        agro_climatic_zone=self.AGRO_ZONES.get(dist, "Coastal & Plains Zone"),
                    )
                    session.add(dim_loc)
                    counts["dim_location"] += 1
            session.flush()

            # 2. Populate DimCrop
            crops = session.query(StagingCropProduction.crop).distinct().all()
            for (crop_name,) in crops:
                if not session.query(DimCrop).filter_by(crop_name=crop_name).first():
                    dim_c = DimCrop(
                        crop_name=crop_name,
                        crop_category="Commercial" if "Cotton" in crop_name or "Chilli" in crop_name else "Foodgrain",
                        major_growing_season="Kharif",
                    )
                    session.add(dim_c)
                    counts["dim_crop"] += 1
            session.flush()

            # 3. Populate DimMarket
            markets = session.query(StagingMandiPrice.market, StagingMandiPrice.district).distinct().all()
            for mkt, dist in markets:
                if not session.query(DimMarket).filter_by(market_name=mkt).first():
                    dim_m = DimMarket(
                        market_name=mkt,
                        district=dist,
                        apmc_code=f"APMC_{dist.upper()[:3]}",
                    )
                    session.add(dim_m)
                    counts["dim_market"] += 1
            session.flush()

            # 4. Populate DimDate
            dates = session.query(StagingMandiPrice.arrival_date).distinct().all()
            for (cal_date,) in dates:
                dt_id = int(cal_date.strftime("%Y%m%d"))
                if not session.query(DimDate).filter_by(date_id=dt_id).first():
                    dim_d = DimDate(
                        date_id=dt_id,
                        calendar_date=cal_date,
                        year=cal_date.year,
                        month=cal_date.month,
                        month_name=cal_date.strftime("%B"),
                        quarter=(cal_date.month - 1) // 3 + 1,
                        season="Rabi" if cal_date.month in [1, 2, 3, 4] else "Kharif",
                    )
                    session.add(dim_d)
                    counts["dim_date"] += 1
            session.flush()

            # 5. Populate FactCropProduction
            loc_map = {loc.district: loc.location_id for loc in session.query(DimLocation).all()}
            crop_map = {c.crop_name: c.crop_id for c in session.query(DimCrop).all()}

            # Populate a generic date for yearly crop records
            default_date_id = 20240101
            if not session.query(DimDate).filter_by(date_id=default_date_id).first():
                session.add(DimDate(
                    date_id=default_date_id,
                    calendar_date=date(2024, 1, 1),
                    year=2024,
                    month=1,
                    month_name="January",
                    quarter=1,
                    season="Kharif",
                ))
                session.flush()

            if session.query(FactCropProduction).count() == 0:
                for stg in session.query(StagingCropProduction).all():
                    loc_id = loc_map.get(stg.district)
                    crp_id = crop_map.get(stg.crop)
                    if loc_id and crp_id:
                        fact = FactCropProduction(
                            date_id=default_date_id,
                            location_id=loc_id,
                            crop_id=crp_id,
                            area_hectares=stg.area_hectares,
                            production_tonnes=stg.production_tonnes,
                            yield_quintal_per_ha=stg.yield_quintal_per_ha,
                        )
                        session.add(fact)
                        counts["facts"] += 1

            # 6. Populate FactSoil
            if session.query(FactSoil).count() == 0:
                for s in session.query(StagingSoil).all():
                    loc_id = loc_map.get(s.district)
                    if loc_id:
                        fact_s = FactSoil(
                            location_id=loc_id,
                            nitrogen_kg_ha=s.available_nitrogen_kg_ha,
                            phosphorus_kg_ha=s.available_phosphorus_kg_ha,
                            potassium_kg_ha=s.available_potassium_kg_ha,
                            soil_ph=s.soil_ph,
                            organic_carbon_pct=s.organic_carbon_pct,
                            electrical_conductivity_dsm=s.electrical_conductivity_dsm,
                            soil_type=s.soil_type,
                        )
                        session.add(fact_s)

            session.commit()
            return counts
        except Exception as e:
            session.rollback()
            logger.error(f"Error during Silver -> Gold transformation: {e}")
            raise e
        finally:
            session.close()


medallion_service = MedallionWarehouseService()
