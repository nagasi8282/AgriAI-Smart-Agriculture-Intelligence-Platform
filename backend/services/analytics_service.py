"""
AgriAI Backend - Analytics Service
Aggregates and filters agricultural data from local Medallion storage or sample datasets.
"""

from typing import List, Dict, Any, Optional
import pandas as pd
from storage.local_storage import local_storage
from backend.schemas.analytics import (
    CropProductionRecord,
    MandiPriceRecord,
    WeatherRecord,
    SoilRecord,
    DashboardSummary,
)


class AnalyticsService:
    def __init__(self):
        self._crop_df: Optional[pd.DataFrame] = None
        self._mandi_df: Optional[pd.DataFrame] = None
        self._weather_df: Optional[pd.DataFrame] = None
        self._soil_df: Optional[pd.DataFrame] = None
        self._load_datasets()

    def _load_datasets(self) -> None:
        """Cache baseline sample datasets in memory for fast analytical querying."""
        try:
            self._crop_df = local_storage.load_sample_dataset("crop_production")
            self._mandi_df = local_storage.load_sample_dataset("mandi_prices")
            self._weather_df = local_storage.load_sample_dataset("weather")
            self._soil_df = local_storage.load_sample_dataset("soil_health")
        except Exception as e:
            # Fallbacks in case datasets are not generated yet
            self._crop_df = pd.DataFrame()
            self._mandi_df = pd.DataFrame()
            self._weather_df = pd.DataFrame()
            self._soil_df = pd.DataFrame()

    def get_dashboard_summary(self) -> DashboardSummary:
        """Compute key agricultural KPIs for the home dashboard."""
        total_crops = len(self._crop_df) if not self._crop_df.empty else 0
        districts = sorted(self._crop_df["district_name"].unique().tolist()) if not self._crop_df.empty else []
        crops = sorted(self._crop_df["crop"].unique().tolist()) if not self._crop_df.empty else []
        latest_date = (
            str(self._mandi_df["arrival_date"].max())
            if not self._mandi_df.empty and "arrival_date" in self._mandi_df.columns
            else "N/A"
        )
        weather_alerts = (
            int((self._weather_df["rainfall_mm"] > 35.0).sum())
            if not self._weather_df.empty and "rainfall_mm" in self._weather_df.columns
            else 0
        )

        return DashboardSummary(
            total_crop_records=total_crops,
            total_districts=len(districts),
            total_crops_tracked=len(crops),
            latest_mandi_update=latest_date,
            weather_alert_count=weather_alerts,
            districts_list=districts,
            crops_list=crops,
        )

    def get_crop_production(
        self,
        district: Optional[str] = None,
        crop: Optional[str] = None,
        season: Optional[str] = None,
        year_start: Optional[int] = None,
        year_end: Optional[int] = None,
    ) -> List[CropProductionRecord]:
        """Filter crop production historical data."""
        if self._crop_df.empty:
            return []

        df = self._crop_df.copy()
        if district:
            df = df[df["district_name"].str.lower() == district.lower()]
        if crop:
            df = df[df["crop"].str.lower() == crop.lower()]
        if season:
            df = df[df["season"].str.lower() == season.lower()]
        if year_start:
            df = df[df["crop_year"] >= year_start]
        if year_end:
            df = df[df["crop_year"] <= year_end]

        records = []
        for _, row in df.iterrows():
            records.append(
                CropProductionRecord(
                    state_name=row["state_name"],
                    district_name=row["district_name"],
                    crop_year=int(row["crop_year"]),
                    season=row["season"],
                    crop=row["crop"],
                    area_hectares=float(row["area_hectares"]),
                    production_tonnes=float(row["production_tonnes"]),
                    yield_quintal_per_ha=float(row["yield_quintal_per_ha"]),
                )
            )
        return records

    def get_mandi_prices(
        self,
        district: Optional[str] = None,
        market: Optional[str] = None,
        commodity: Optional[str] = None,
    ) -> List[MandiPriceRecord]:
        """Filter AGMARKNET mandi market prices."""
        if self._mandi_df.empty:
            return []

        df = self._mandi_df.copy()
        if district:
            df = df[df["district"].str.lower() == district.lower()]
        if market:
            df = df[df["market"].str.lower() == market.lower()]
        if commodity:
            df = df[df["commodity"].str.lower() == commodity.lower()]

        records = []
        for _, row in df.iterrows():
            records.append(
                MandiPriceRecord(
                    state=row["state"],
                    district=row["district"],
                    market=row["market"],
                    commodity=row["commodity"],
                    variety=row.get("variety", "Standard"),
                    arrival_date=str(row["arrival_date"]),
                    min_price_inr=float(row["min_price_inr"]),
                    max_price_inr=float(row["max_price_inr"]),
                    modal_price_inr=float(row["modal_price_inr"]),
                    arrival_tonnes=float(row.get("arrival_tonnes", 0.0)),
                )
            )
        return records

    def get_weather(self, district: Optional[str] = None) -> List[WeatherRecord]:
        """Fetch meteorological records."""
        if self._weather_df.empty:
            return []

        df = self._weather_df.copy()
        if district:
            df = df[df["district"].str.lower() == district.lower()]

        records = []
        for _, row in df.iterrows():
            records.append(
                WeatherRecord(
                    district=row["district"],
                    date=str(row["date"]),
                    temp_max_c=float(row["temp_max_c"]),
                    temp_min_c=float(row["temp_min_c"]),
                    temp_mean_c=float(row["temp_mean_c"]),
                    rainfall_mm=float(row["rainfall_mm"]),
                    relative_humidity_pct=float(row["relative_humidity_pct"]),
                    wind_speed_kmh=float(row["wind_speed_kmh"]),
                    is_forecast=bool(row.get("is_forecast", False)),
                    condition=str(row.get("condition", "Normal")),
                )
            )
        return records

    def get_soil(self, district: Optional[str] = None) -> List[SoilRecord]:
        """Fetch soil health and nutrient indicators."""
        if self._soil_df.empty:
            return []

        df = self._soil_df.copy()
        if district:
            df = df[df["district"].str.lower() == district.lower()]

        records = []
        for _, row in df.iterrows():
            records.append(
                SoilRecord(
                    district=row["district"],
                    soil_type=row["soil_type"],
                    available_nitrogen_kg_ha=float(row["available_nitrogen_kg_ha"]),
                    available_phosphorus_kg_ha=float(row["available_phosphorus_kg_ha"]),
                    available_potassium_kg_ha=float(row["available_potassium_kg_ha"]),
                    soil_ph=float(row["soil_ph"]),
                    organic_carbon_pct=float(row["organic_carbon_pct"]),
                    electrical_conductivity_dsm=float(row["electrical_conductivity_dsm"]),
                    nitrogen_category=row.get("nitrogen_category", "Medium"),
                    phosphorus_category=row.get("phosphorus_category", "Medium"),
                    potassium_category=row.get("potassium_category", "Medium"),
                )
            )
        return records


analytics_service = AnalyticsService()
