# dbt_agri: Data Build Tool (dbt) Transformations for AgriAI

This directory contains dbt transformation models for the AgriAI Medallion Data Warehouse in Snowflake and PostgreSQL.

## Structure
- `models/staging/`: Silver layer models performing type casting, deduplication, null-handling, and district/crop canonicalization.
- `models/marts/`: Gold layer dimensional models (`dim_location`, `dim_crop`, `dim_date`, `fact_crop_production`, `fact_mandi_price`, etc.).
- `tests/`: Data quality assertions verifying primary keys, price ranges, non-negative area/yield, and referential integrity.

## Running dbt
```bash
# Verify connection
dbt debug

# Run staging models
dbt run --select staging

# Run analytical marts
dbt run --select marts

# Execute data quality tests
dbt test
```
