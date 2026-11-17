-- ==============================================================================
-- AgriAI Snowflake Cloud Warehouse Setup Script
-- Part 4: Gold Layer Dimensional Star Schema (Analytical Marts)
-- ==============================================================================

USE DATABASE AGRIAI_DW;
USE SCHEMA GOLD_MARTS;

-- 1. Date Dimension
CREATE OR REPLACE TABLE DIM_DATE (
    date_id INT PRIMARY KEY,
    calendar_date DATE UNIQUE NOT NULL,
    year INT NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20),
    quarter INT NOT NULL,
    day_of_month INT,
    day_of_week VARCHAR(15),
    is_weekend BOOLEAN
);

-- 2. Location Dimension (Districts of Andhra Pradesh)
CREATE OR REPLACE TABLE DIM_LOCATION (
    location_id INT PRIMARY KEY,
    state VARCHAR(50) NOT NULL,
    district VARCHAR(100) NOT NULL,
    agro_climatic_zone VARCHAR(100),
    latitude NUMBER(8,4),
    longitude NUMBER(8,4)
);

-- 3. Crop Dimension
CREATE OR REPLACE TABLE DIM_CROP (
    crop_id INT PRIMARY KEY,
    crop_name VARCHAR(100) NOT NULL,
    crop_category VARCHAR(50),
    botanical_name VARCHAR(100),
    growing_season VARCHAR(50)
);

-- 4. Market Dimension (APMC Yards)
CREATE OR REPLACE TABLE DIM_MARKET (
    market_id INT PRIMARY KEY,
    market_name VARCHAR(150) NOT NULL,
    district VARCHAR(100) NOT NULL,
    apmc_code VARCHAR(50)
);

-- 5. Fact: Crop Production
CREATE OR REPLACE TABLE FACT_CROP_PRODUCTION (
    production_id BIGINT AUTOINCREMENT PRIMARY KEY,
    date_id INT FOREIGN KEY REFERENCES DIM_DATE(date_id),
    location_id INT FOREIGN KEY REFERENCES DIM_LOCATION(location_id),
    crop_id INT FOREIGN KEY REFERENCES DIM_CROP(crop_id),
    area_hectares NUMBER(12,2),
    production_tonnes NUMBER(12,2),
    yield_quintal_per_ha NUMBER(10,2)
);

-- 6. Fact: Mandi Prices
CREATE OR REPLACE TABLE FACT_MANDI_PRICE (
    mandi_price_id BIGINT AUTOINCREMENT PRIMARY KEY,
    date_id INT FOREIGN KEY REFERENCES DIM_DATE(date_id),
    location_id INT FOREIGN KEY REFERENCES DIM_LOCATION(location_id),
    crop_id INT FOREIGN KEY REFERENCES DIM_CROP(crop_id),
    market_id INT FOREIGN KEY REFERENCES DIM_MARKET(market_id),
    min_price_inr NUMBER(10,2),
    max_price_inr NUMBER(10,2),
    modal_price_inr NUMBER(10,2),
    arrival_tonnes NUMBER(10,2)
);

-- 7. Fact: Weather Observations
CREATE OR REPLACE TABLE FACT_WEATHER (
    weather_id BIGINT AUTOINCREMENT PRIMARY KEY,
    date_id INT FOREIGN KEY REFERENCES DIM_DATE(date_id),
    location_id INT FOREIGN KEY REFERENCES DIM_LOCATION(location_id),
    temp_max_c NUMBER(5,2),
    temp_min_c NUMBER(5,2),
    temp_mean_c NUMBER(5,2),
    rainfall_mm NUMBER(8,2),
    relative_humidity_pct NUMBER(5,2),
    wind_speed_kmh NUMBER(5,2)
);

-- 8. Fact: Soil Health Profile
CREATE OR REPLACE TABLE FACT_SOIL (
    soil_id BIGINT AUTOINCREMENT PRIMARY KEY,
    location_id INT FOREIGN KEY REFERENCES DIM_LOCATION(location_id),
    nitrogen_kg_ha NUMBER(8,2),
    phosphorus_kg_ha NUMBER(8,2),
    potassium_kg_ha NUMBER(8,2),
    soil_ph NUMBER(4,2),
    organic_carbon_pct NUMBER(4,2),
    electrical_conductivity_dsm NUMBER(5,2)
);
