-- ==============================================================================
-- AgriAI Snowflake Cloud Warehouse Setup Script
-- Part 2: Bronze Layer Raw Tables (Landing Zone)
-- ==============================================================================

USE DATABASE AGRIAI_DW;
USE SCHEMA BRONZE_RAW;

-- Raw Crop Production Table
CREATE OR REPLACE TABLE RAW_CROP_PRODUCTION (
    _ingest_id VARCHAR(64) DEFAULT UUID_STRING(),
    _ingested_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    _source_file VARCHAR(256),
    raw_payload VARIANT,
    state_name VARCHAR(100),
    district_name VARCHAR(100),
    crop_year NUMBER(4,0),
    season VARCHAR(50),
    crop VARCHAR(100),
    area_hectares NUMBER(12,2),
    production_tonnes NUMBER(12,2),
    yield_quintal_per_ha NUMBER(10,2)
);

-- Raw AGMARKNET Mandi Prices Table
CREATE OR REPLACE TABLE RAW_MANDI_PRICES (
    _ingest_id VARCHAR(64) DEFAULT UUID_STRING(),
    _ingested_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    _source_file VARCHAR(256),
    raw_payload VARIANT,
    state VARCHAR(100),
    district VARCHAR(100),
    market VARCHAR(150),
    commodity VARCHAR(100),
    variety VARCHAR(100),
    arrival_date DATE,
    min_price_inr NUMBER(10,2),
    max_price_inr NUMBER(10,2),
    modal_price_inr NUMBER(10,2),
    arrival_tonnes NUMBER(10,2)
);

-- Raw Weather Observations Table
CREATE OR REPLACE TABLE RAW_WEATHER (
    _ingest_id VARCHAR(64) DEFAULT UUID_STRING(),
    _ingested_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    _source_file VARCHAR(256),
    raw_payload VARIANT,
    district VARCHAR(100),
    observation_date DATE,
    temp_max_c NUMBER(5,2),
    temp_min_c NUMBER(5,2),
    temp_mean_c NUMBER(5,2),
    rainfall_mm NUMBER(8,2),
    relative_humidity_pct NUMBER(5,2),
    wind_speed_kmh NUMBER(5,2),
    is_forecast BOOLEAN DEFAULT FALSE,
    condition VARCHAR(50)
);

-- Raw Soil Health Records Table
CREATE OR REPLACE TABLE RAW_SOIL (
    _ingest_id VARCHAR(64) DEFAULT UUID_STRING(),
    _ingested_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    district VARCHAR(100),
    soil_type VARCHAR(100),
    available_nitrogen_kg_ha NUMBER(8,2),
    available_phosphorus_kg_ha NUMBER(8,2),
    available_potassium_kg_ha NUMBER(8,2),
    soil_ph NUMBER(4,2),
    organic_carbon_pct NUMBER(4,2),
    electrical_conductivity_dsm NUMBER(5,2)
);
