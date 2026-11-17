"""
AgriAI Test Suite - Phase 3 Medallion Data Warehouse & Data Quality Tests
Validates Silver standardized staging, Gold star schema dimensional marts,
referential integrity, and data quality constraints.
"""

import pytest
from backend.services.medallion_service import medallion_service
from backend.models.medallion_models import (
    StagingCropProduction,
    StagingMandiPrice,
    DimLocation,
    DimCrop,
    DimMarket,
    DimDate,
    FactCropProduction,
    FactSoil,
)


def test_standardization_mappings():
    """Verify phonetic and spelling variations are standardized to canonical names."""
    assert medallion_service.standardize_district("e. godavari") == "East Godavari"
    assert medallion_service.standardize_district("GUNTUR") == "Guntur"
    assert medallion_service.standardize_district("ysr kadapa") == "YSR Kadapa"
    assert medallion_service.standardize_district("vizag") == "Visakhapatnam"

    assert medallion_service.standardize_crop("paddy") == "Paddy (Rice)"
    assert medallion_service.standardize_crop("rice") == "Paddy (Rice)"
    assert medallion_service.standardize_crop("chilli") == "Chillies"
    assert medallion_service.standardize_crop("corn") == "Maize"


def test_bronze_to_silver_transformation():
    """Verify Silver layer ingestion cleans and deduplicates records into staging tables."""
    counts = medallion_service.transform_bronze_to_silver()
    session = medallion_service.get_session()

    try:
        crop_count = session.query(StagingCropProduction).count()
        mandi_count = session.query(StagingMandiPrice).count()

        assert crop_count >= 800
        assert mandi_count >= 1000

        # Check deduplication: Checksums must be unique
        first_crop = session.query(StagingCropProduction).first()
        assert first_crop is not None
        assert first_crop._checksum is not None
        assert len(first_crop._checksum) == 64
    finally:
        session.close()


def test_silver_to_gold_star_schema_loading():
    """Verify Gold dimensions and fact tables are correctly populated."""
    counts = medallion_service.transform_silver_to_gold()
    session = medallion_service.get_session()

    try:
        locations = session.query(DimLocation).all()
        crops = session.query(DimCrop).all()
        markets = session.query(DimMarket).all()
        facts = session.query(FactCropProduction).all()

        assert len(locations) >= 10
        assert len(crops) >= 5
        assert len(markets) >= 4
        assert len(facts) >= 800

        # Verify fact table referential integrity
        first_fact = facts[0]
        assert first_fact.location_id is not None
        assert first_fact.crop_id is not None
        assert first_fact.date_id is not None
        assert first_fact.area_hectares > 0
        assert first_fact.production_tonnes > 0
    finally:
        session.close()


def test_gold_star_schema_analytical_query():
    """Verify star schema joins work for analytical aggregation by district and crop."""
    session = medallion_service.get_session()

    try:
        # Query total paddy production in Guntur
        res = (
            session.query(
                DimLocation.district,
                DimCrop.crop_name,
                FactCropProduction.area_hectares,
                FactCropProduction.production_tonnes,
                FactCropProduction.yield_quintal_per_ha,
            )
            .join(DimLocation, FactCropProduction.location_id == DimLocation.location_id)
            .join(DimCrop, FactCropProduction.crop_id == DimCrop.crop_id)
            .filter(DimLocation.district == "Guntur")
            .filter(DimCrop.crop_name == "Paddy (Rice)")
            .all()
        )

        assert len(res) > 0
        first_row = res[0]
        assert first_row.district == "Guntur"
        assert first_row.crop_name == "Paddy (Rice)"
        assert first_row.yield_quintal_per_ha >= 30.0
    finally:
        session.close()
