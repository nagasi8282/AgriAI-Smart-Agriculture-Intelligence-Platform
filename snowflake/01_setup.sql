-- ==============================================================================
-- AgriAI Snowflake Cloud Warehouse Setup Script
-- Part 1: Administrative Roles, Warehouses, Databases & Schemas
-- ==============================================================================

USE ROLE ACCOUNTADMIN;

-- 1. Create Dedicated Virtual Warehouse
CREATE WAREHOUSE IF NOT EXISTS AGRIAI_WH
    WITH WAREHOUSE_SIZE = 'XSMALL'
    AUTO_SUSPEND = 180
    AUTO_RESUME = TRUE
    INITIALLY_SUSPENDED = TRUE
    COMMENT = 'Virtual warehouse for AgriAI data engineering pipelines and analytics';

-- 2. Create Analytics Database
CREATE DATABASE IF NOT EXISTS AGRIAI_DW
    COMMENT = 'Centralized Cloud Data Warehouse for AgriAI Agriculture Intelligence';

-- 3. Create Medallion Schemas
USE DATABASE AGRIAI_DW;

CREATE SCHEMA IF NOT EXISTS BRONZE_RAW
    COMMENT = 'Raw ingested agricultural datasets (immutable landing zone)';

CREATE SCHEMA IF NOT EXISTS SILVER_STAGING
    COMMENT = 'Cleaned, conformed, and standardized data models';

CREATE SCHEMA IF NOT EXISTS GOLD_MARTS
    COMMENT = 'Dimensional star schema marts for dashboards, ML feature stores, and BI';

-- 4. Create Pipeline Service Role
CREATE ROLE IF NOT EXISTS AGRIAI_PIPELINE_ROLE
    COMMENT = 'Service role for Airflow and dbt data transformation pipelines';

GRANT USAGE ON WAREHOUSE AGRIAI_WH TO ROLE AGRIAI_PIPELINE_ROLE;
GRANT USAGE, OPERATE ON WAREHOUSE AGRIAI_WH TO ROLE AGRIAI_PIPELINE_ROLE;
GRANT USAGE ON DATABASE AGRIAI_DW TO ROLE AGRIAI_PIPELINE_ROLE;
GRANT ALL ON SCHEMA AGRIAI_DW.BRONZE_RAW TO ROLE AGRIAI_PIPELINE_ROLE;
GRANT ALL ON SCHEMA AGRIAI_DW.SILVER_STAGING TO ROLE AGRIAI_PIPELINE_ROLE;
GRANT ALL ON SCHEMA AGRIAI_DW.GOLD_MARTS TO ROLE AGRIAI_PIPELINE_ROLE;
