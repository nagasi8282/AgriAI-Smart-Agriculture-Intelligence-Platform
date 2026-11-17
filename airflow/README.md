# Apache Airflow Orchestration for AgriAI

This directory contains the production Apache Airflow DAG definitions and orchestration configurations for the AgriAI data pipelines.

## Orchestration Architecture
- **DAG**: `agri_daily_etl_pipeline`
- **Schedule**: `0 6 * * *` (06:00 UTC / 11:30 AM IST Daily)
- **Retry Policy**: 3 retries with 5-minute exponential backoff
- **Execution Workflow**:
  `start_pipeline` -> Ingest [Crops, Mandi, Weather] -> `validate_bronze_records` -> `run_dbt_staging` -> `run_dbt_marts` -> `run_data_quality_tests` -> `end_pipeline`

## Local Airflow Startup
To launch Airflow locally via Docker Compose:
```bash
cd airflow
docker-compose up -d
```
Access the Airflow Web UI at: `http://localhost:8080` (Default: `airflow` / `airflow`).
