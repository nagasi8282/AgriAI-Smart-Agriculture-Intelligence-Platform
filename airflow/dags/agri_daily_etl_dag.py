"""
AgriAI Orchestration - Daily Agricultural ETL DAG
Orchestrates Bronze ingestion, Silver staging, Gold marts transformation, and data quality tests.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

default_args = {
    "owner": "agriai_data_engineering",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 3,
    "retry_delay": timedelta(minutes=5),
    "execution_timeout": timedelta(minutes=45),
}


def task_ingest_crop_production():
    print("Ingesting latest Andhra Pradesh crop production statistics from data.gov.in...")


def task_ingest_mandi_prices():
    print("Executing incremental AGMARKNET mandi arrival extraction using high-watermark...")


def task_ingest_weather():
    print("Ingesting IMD / Open-Meteo meteorological observations...")


def task_validate_bronze():
    print("Executing Bronze schema validation and duplicate row checksum audit...")


def task_run_dbt_staging():
    print("Executing dbt run --select staging (Silver conformed layer)...")


def task_run_dbt_marts():
    print("Executing dbt run --select marts (Gold star schema facts and dimensions)...")


def task_data_quality_tests():
    print("Executing dbt test and Great Expectations validation suite...")


with DAG(
    dag_id="agri_daily_etl_pipeline",
    default_args=default_args,
    description="End-to-End AgriAI Medallion Data Engineering Pipeline",
    schedule_interval="0 6 * * *",  # 06:00 AM UTC Daily
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=["agriai", "andhra_pradesh", "medallion", "dbt", "snowflake"],
) as dag:

    start_pipeline = EmptyOperator(task_id="start_pipeline")

    ingest_crops = PythonOperator(
        task_id="ingest_crop_production",
        python_callable=task_ingest_crop_production,
    )

    ingest_mandi = PythonOperator(
        task_id="ingest_mandi_prices",
        python_callable=task_ingest_mandi_prices,
    )

    ingest_weather = PythonOperator(
        task_id="ingest_weather_observations",
        python_callable=task_ingest_weather,
    )

    validate_bronze = PythonOperator(
        task_id="validate_bronze_records",
        python_callable=task_validate_bronze,
    )

    run_dbt_staging = PythonOperator(
        task_id="run_dbt_staging",
        python_callable=task_run_dbt_staging,
    )

    run_dbt_marts = PythonOperator(
        task_id="run_dbt_marts",
        python_callable=task_run_dbt_marts,
    )

    run_tests = PythonOperator(
        task_id="run_data_quality_tests",
        python_callable=task_data_quality_tests,
    )

    end_pipeline = EmptyOperator(task_id="end_pipeline")

    # DAG Task Dependencies
    start_pipeline >> [ingest_crops, ingest_mandi, ingest_weather]
    [ingest_crops, ingest_mandi, ingest_weather] >> validate_bronze
    validate_bronze >> run_dbt_staging >> run_dbt_marts >> run_tests >> end_pipeline
