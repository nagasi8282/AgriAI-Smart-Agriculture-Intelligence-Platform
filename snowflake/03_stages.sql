-- ==============================================================================
-- AgriAI Snowflake Cloud Warehouse Setup Script
-- Part 3: File Formats and S3 / Internal Stages
-- ==============================================================================

USE DATABASE AGRIAI_DW;
USE SCHEMA BRONZE_RAW;

-- 1. Create File Formats for CSV and Parquet
CREATE OR REPLACE FILE FORMAT FF_CSV_COMMA
    TYPE = 'CSV'
    COMPRESSION = 'AUTO'
    FIELD_DELIMITER = ','
    RECORD_DELIMITER = '\n'
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    TRIM_SPACE = TRUE
    ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
    NULL_IF = ('', 'NULL', 'null', 'NA');

CREATE OR REPLACE FILE FORMAT FF_PARQUET
    TYPE = 'PARQUET'
    COMPRESSION = 'SNAPPY';

-- 2. Internal Named Stage for Local Uploads / CLI Ingestion
CREATE OR REPLACE STAGE STG_INTERNAL_AGRICULTURE
    FILE_FORMAT = FF_CSV_COMMA
    COMMENT = 'Internal stage for manual CSV/JSON uploads via SnowSQL';

-- 3. External Stage pointing to AWS S3 Data Lake (Parameterized template)
-- Note: Replace AWS IAM credentials or Storage Integration with production ARN
CREATE OR REPLACE STAGE STG_S3_AGRIAI_LAKE
    URL = 's3://agriai-data-lake-ap/raw/'
    -- STORAGE_INTEGRATION = s3_int_agriai
    FILE_FORMAT = FF_PARQUET
    COMMENT = 'External S3 stage reading raw partitioned data from AWS S3';
