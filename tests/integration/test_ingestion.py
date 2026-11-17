"""
AgriAI Test Suite - Phase 2 Ingestion Pipeline & Quality Integration Tests
Validates full and incremental ingestion, watermark tracking, schema enforcement,
and quarantine isolation across all agricultural data connectors.
"""

import pytest
from pathlib import Path
from ingestion.crop_ingestion import crop_connector
from ingestion.mandi_ingestion import mandi_connector
from ingestion.weather_ingestion import weather_connector
from ingestion.soil_ingestion import soil_connector
from ingestion.common.watermark import watermark_manager
from ingestion.common.validator import data_validator
from storage.local_storage import local_storage


def test_crop_production_full_and_incremental_ingestion():
    """Verify crop ingestion executes full load, advances watermark, and handles incremental runs."""
    # Reset watermark to force full load
    watermark_manager.reset_watermark("crop_production")

    # 1. Full Ingestion Run
    result = crop_connector.run_pipeline(full_load=True)
    assert result["status"] == "success"
    assert result["rows_ingested"] > 0
    assert result["quarantined"] == 0

    # Verify watermark updated
    new_watermark = watermark_manager.get_watermark("crop_production")
    assert new_watermark is not None
    assert int(new_watermark) >= 2023

    # 2. Incremental Run (should ingest 0 rows since watermark is up-to-date)
    incremental_result = crop_connector.run_pipeline(full_load=False)
    assert incremental_result["status"] == "success"
    assert incremental_result["rows_ingested"] == 0


def test_mandi_prices_quarantine_routing():
    """Verify mandi records violating min_price <= modal_price <= max_price are quarantined."""
    # Test dataset with intentional price anomalies
    anomalous_records = [
        {
            "state": "Andhra Pradesh",
            "district": "Guntur",
            "market": "Guntur APMC",
            "commodity": "Chillies",
            "variety": "Common",
            "arrival_date": "2024-05-01",
            "min_price_inr": 22000.0,  # Min greater than Max!
            "max_price_inr": 18000.0,
            "modal_price_inr": 20000.0,
            "arrival_tonnes": 50.0,
        },
        {
            "state": "Andhra Pradesh",
            "district": "Guntur",
            "market": "Guntur APMC",
            "commodity": "Chillies",
            "variety": "Common",
            "arrival_date": "2024-05-01",
            "min_price_inr": 17000.0,
            "max_price_inr": 21000.0,
            "modal_price_inr": 19000.0,  # Valid record
            "arrival_tonnes": 60.0,
        },
    ]

    valid, rejected = data_validator.validate_mandi_prices(anomalous_records)
    assert len(valid) == 1
    assert len(rejected) == 1
    assert "Price band violation" in rejected[0]["_rejection_reasons"][0]

    # Verify quarantine file generation
    q_path = data_validator.route_to_quarantine("mandi_prices", rejected)
    assert q_path.exists()
    assert q_path.stat().st_size > 0


def test_weather_quality_validation():
    """Verify meteorological records with temperature inverted ranges are flagged."""
    anomalous_weather = [
        {
            "district": "Kurnool",
            "date": "2024-05-01",
            "temp_max_c": 22.0,  # Inverted: max lower than min!
            "temp_min_c": 35.0,
            "temp_mean_c": 28.5,
            "rainfall_mm": -5.0,  # Negative rainfall!
            "relative_humidity_pct": 115.0,  # Out of 0-100% bounds!
            "wind_speed_kmh": 12.0,
        }
    ]

    valid, rejected = data_validator.validate_weather(anomalous_weather)
    assert len(valid) == 0
    assert len(rejected) == 1
    reasons = rejected[0]["_rejection_reasons"]
    assert len(reasons) >= 3


def test_soil_health_ingestion():
    """Verify soil health ingestion pipeline loads AP district profiles to Bronze."""
    result = soil_connector.run_pipeline()
    assert result["status"] == "success"
    assert result["rows_ingested"] >= 10
    assert result["quarantined"] == 0

    # Verify Bronze files exist
    bronze_files = local_storage.list_raw_files("soil")
    assert len(bronze_files) > 0


def test_bronze_lake_directory_partitioning():
    """Verify Bronze layer strictly follows partitioned directory structure: year={YYYY}/month={MM}/."""
    mandi_files = local_storage.list_raw_files("crop_production")
    assert len(mandi_files) > 0
    first_path = str(mandi_files[0])
    assert "year=" in first_path
    assert "month=" in first_path
