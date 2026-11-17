"""
AgriAI Medallion Data Warehouse - SQLAlchemy Relational & Dimensional Models
Defines Silver staging tables and Gold star schema dimensional marts.
Compatible across SQLite (local development/testing) and PostgreSQL/Snowflake (production).
"""

from datetime import datetime, date, timezone
from typing import Optional
from sqlalchemy import (
    Column,
    Integer,
    BigInteger,
    String,
    Float,
    Date,
    DateTime,
    Boolean,
    ForeignKey,
    Index,
    Numeric,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


# ==============================================================================
# SILVER LAYER: Cleaned, Standardized & Conformed Staging Tables
# ==============================================================================

class StagingCropProduction(Base):
    __tablename__ = "silver_crop_production"

    id = Column(Integer, primary_key=True, autoincrement=True)
    state = Column(String(50), nullable=False, default="Andhra Pradesh")
    district = Column(String(100), nullable=False, index=True)
    crop_year = Column(Integer, nullable=False, index=True)
    season = Column(String(50), nullable=False)
    crop = Column(String(100), nullable=False, index=True)
    area_hectares = Column(Float, nullable=False)
    production_tonnes = Column(Float, nullable=False)
    yield_quintal_per_ha = Column(Float, nullable=False)
    _checksum = Column(String(64), unique=True, index=True)
    _ingested_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class StagingMandiPrice(Base):
    __tablename__ = "silver_mandi_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    state = Column(String(50), nullable=False, default="Andhra Pradesh")
    district = Column(String(100), nullable=False, index=True)
    market = Column(String(150), nullable=False, index=True)
    commodity = Column(String(100), nullable=False, index=True)
    variety = Column(String(100), default="Standard")
    arrival_date = Column(Date, nullable=False, index=True)
    min_price_inr = Column(Float, nullable=False)
    max_price_inr = Column(Float, nullable=False)
    modal_price_inr = Column(Float, nullable=False)
    arrival_tonnes = Column(Float, default=0.0)
    _checksum = Column(String(64), unique=True, index=True)
    _ingested_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class StagingWeather(Base):
    __tablename__ = "silver_weather"

    id = Column(Integer, primary_key=True, autoincrement=True)
    district = Column(String(100), nullable=False, index=True)
    observation_date = Column(Date, nullable=False, index=True)
    temp_max_c = Column(Float, nullable=False)
    temp_min_c = Column(Float, nullable=False)
    temp_mean_c = Column(Float, nullable=False)
    rainfall_mm = Column(Float, nullable=False)
    relative_humidity_pct = Column(Float, nullable=False)
    wind_speed_kmh = Column(Float, nullable=False)
    is_forecast = Column(Boolean, default=False)
    condition = Column(String(50), default="Normal")
    _checksum = Column(String(64), unique=True, index=True)
    _ingested_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


class StagingSoil(Base):
    __tablename__ = "silver_soil"

    id = Column(Integer, primary_key=True, autoincrement=True)
    district = Column(String(100), nullable=False, unique=True, index=True)
    soil_type = Column(String(100), nullable=False)
    available_nitrogen_kg_ha = Column(Float, nullable=False)
    available_phosphorus_kg_ha = Column(Float, nullable=False)
    available_potassium_kg_ha = Column(Float, nullable=False)
    soil_ph = Column(Float, nullable=False)
    organic_carbon_pct = Column(Float, nullable=False)
    electrical_conductivity_dsm = Column(Float, nullable=False)
    nitrogen_category = Column(String(20))
    phosphorus_category = Column(String(20))
    potassium_category = Column(String(20))
    _checksum = Column(String(64), unique=True)
    _ingested_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))


# ==============================================================================
# GOLD LAYER: Dimensional Star Schema Marts
# ==============================================================================

class DimDate(Base):
    __tablename__ = "gold_dim_date"

    date_id = Column(Integer, primary_key=True)  # YYYYMMDD
    calendar_date = Column(Date, unique=True, nullable=False, index=True)
    year = Column(Integer, nullable=False, index=True)
    month = Column(Integer, nullable=False)
    month_name = Column(String(20), nullable=False)
    quarter = Column(Integer, nullable=False)
    season = Column(String(30))  # Kharif, Rabi, Summer


class DimLocation(Base):
    __tablename__ = "gold_dim_location"

    location_id = Column(Integer, primary_key=True, autoincrement=True)
    state = Column(String(50), nullable=False)
    district = Column(String(100), unique=True, nullable=False, index=True)
    agro_climatic_zone = Column(String(100))
    latitude = Column(Float)
    longitude = Column(Float)


class DimCrop(Base):
    __tablename__ = "gold_dim_crop"

    crop_id = Column(Integer, primary_key=True, autoincrement=True)
    crop_name = Column(String(100), unique=True, nullable=False, index=True)
    crop_category = Column(String(50))  # Cereal, Cash Crop, Oilseed, Pulse
    botanical_name = Column(String(100))
    major_growing_season = Column(String(50))


class DimMarket(Base):
    __tablename__ = "gold_dim_market"

    market_id = Column(Integer, primary_key=True, autoincrement=True)
    market_name = Column(String(150), unique=True, nullable=False, index=True)
    district = Column(String(100), nullable=False, index=True)
    apmc_code = Column(String(50))


class FactCropProduction(Base):
    __tablename__ = "gold_fact_crop_production"

    production_id = Column(Integer, primary_key=True, autoincrement=True)
    date_id = Column(Integer, ForeignKey("gold_dim_date.date_id"), nullable=False, index=True)
    location_id = Column(Integer, ForeignKey("gold_dim_location.location_id"), nullable=False, index=True)
    crop_id = Column(Integer, ForeignKey("gold_dim_crop.crop_id"), nullable=False, index=True)
    area_hectares = Column(Float, nullable=False)
    production_tonnes = Column(Float, nullable=False)
    yield_quintal_per_ha = Column(Float, nullable=False)

    # Relationships
    date = relationship("DimDate")
    location = relationship("DimLocation")
    crop = relationship("DimCrop")


class FactMandiPrice(Base):
    __tablename__ = "gold_fact_mandi_price"

    mandi_price_id = Column(Integer, primary_key=True, autoincrement=True)
    date_id = Column(Integer, ForeignKey("gold_dim_date.date_id"), nullable=False, index=True)
    location_id = Column(Integer, ForeignKey("gold_dim_location.location_id"), nullable=False, index=True)
    crop_id = Column(Integer, ForeignKey("gold_dim_crop.crop_id"), nullable=False, index=True)
    market_id = Column(Integer, ForeignKey("gold_dim_market.market_id"), nullable=False, index=True)
    min_price_inr = Column(Float, nullable=False)
    max_price_inr = Column(Float, nullable=False)
    modal_price_inr = Column(Float, nullable=False)
    arrival_tonnes = Column(Float, default=0.0)

    # Relationships
    date = relationship("DimDate")
    location = relationship("DimLocation")
    crop = relationship("DimCrop")
    market = relationship("DimMarket")


class FactWeather(Base):
    __tablename__ = "gold_fact_weather"

    weather_id = Column(Integer, primary_key=True, autoincrement=True)
    date_id = Column(Integer, ForeignKey("gold_dim_date.date_id"), nullable=False, index=True)
    location_id = Column(Integer, ForeignKey("gold_dim_location.location_id"), nullable=False, index=True)
    temp_max_c = Column(Float, nullable=False)
    temp_min_c = Column(Float, nullable=False)
    temp_mean_c = Column(Float, nullable=False)
    rainfall_mm = Column(Float, nullable=False)
    relative_humidity_pct = Column(Float, nullable=False)
    wind_speed_kmh = Column(Float, nullable=False)

    # Relationships
    date = relationship("DimDate")
    location = relationship("DimLocation")


class FactSoil(Base):
    __tablename__ = "gold_fact_soil"

    soil_id = Column(Integer, primary_key=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey("gold_dim_location.location_id"), unique=True, nullable=False, index=True)
    nitrogen_kg_ha = Column(Float, nullable=False)
    phosphorus_kg_ha = Column(Float, nullable=False)
    potassium_kg_ha = Column(Float, nullable=False)
    soil_ph = Column(Float, nullable=False)
    organic_carbon_pct = Column(Float, nullable=False)
    electrical_conductivity_dsm = Column(Float, nullable=False)
    soil_type = Column(String(100), nullable=False)

    # Relationships
    location = relationship("DimLocation")
