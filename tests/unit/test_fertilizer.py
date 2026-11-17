"""
AgriAI Test Suite - Fertilizer Recommendation & Agronomic Engine Tests
Validates scientific nutrient balancing, commercial fertilizer bag calculations,
ML formulation classification, and REST API contracts.
"""

import pytest
from fastapi.testclient import TestClient

from backend.main import app
from ml.fertilizer_recommendation.agronomic_engine import agronomic_engine
from ml.fertilizer_recommendation.predict import fertilizer_predictor
from backend.schemas.predictions import FertilizerSupportRequest
from backend.services.prediction_service import prediction_service

client = TestClient(app)


def test_agronomic_engine_crop_rdf():
    """Verify official ANGRAU RDF values for Andhra Pradesh crops."""
    paddy_rdf = agronomic_engine.get_crop_rdf("Paddy (Rice)")
    assert paddy_rdf["N"] == 120.0
    assert paddy_rdf["P"] == 60.0
    assert paddy_rdf["K"] == 40.0
    assert paddy_rdf["zinc_needed"] is True
    assert paddy_rdf["splits"] == 3

    cotton_rdf = agronomic_engine.get_crop_rdf("Cotton")
    assert cotton_rdf["N"] == 150.0
    assert cotton_rdf["splits"] == 4


def test_agronomic_engine_nutrient_classification():
    """Verify Soil Health Card low/medium/high thresholds."""
    assert "Low" in agronomic_engine.classify_nutrient("N", 200.0)
    assert "Medium" in agronomic_engine.classify_nutrient("N", 350.0)
    assert "High" in agronomic_engine.classify_nutrient("N", 600.0)

    assert "Low" in agronomic_engine.classify_nutrient("P", 8.0)
    assert "Medium" in agronomic_engine.classify_nutrient("P", 18.0)
    assert "High" in agronomic_engine.classify_nutrient("P", 35.0)


def test_agronomic_engine_dosage_calculation():
    """Test stoichiometric product calculation for DAP, Urea, and MOP."""
    res = agronomic_engine.calculate_dosage(
        crop="Paddy (Rice)",
        nitrogen=220.0,      # Low N -> 1.25x base
        phosphorus=20.0,     # Medium P -> 1.0x base
        potassium=200.0,     # Medium K -> 1.0x base
        soil_ph=7.2,
        area_hectares=1.0,
    )
    products = {p["name"]: p for p in res["fertilizer_products"]}
    assert "Urea (46% N)" in products
    assert "DAP (18% N, 46% P2O5)" in products
    assert "MOP (60% K2O)" in products

    # DAP needed for 60 kg P2O5 = 60 / 0.46 ~= 130.4 kg
    assert pytest.approx(products["DAP (18% N, 46% P2O5)"]["quantity_kg"], rel=1e-1) == 130.4
    # MOP needed for 40 kg K2O = 40 / 0.60 ~= 66.7 kg
    assert pytest.approx(products["MOP (60% K2O)"]["quantity_kg"], rel=1e-1) == 66.7

    # Split schedule contains 3 stages for paddy
    assert len(res["application_schedule"]) == 3
    # Zinc sulphate should be indicated for paddy
    assert len(res["micronutrients"]) > 0


def test_agronomic_engine_ph_amendments():
    """Test soil amendments for acidic (lime) and alkaline (gypsum) conditions."""
    acidic = agronomic_engine.calculate_dosage(
        crop="Groundnut", nitrogen=150, phosphorus=15, potassium=150, soil_ph=5.4, area_hectares=2.0
    )
    assert acidic["soil_amendment"] is not None
    assert "Lime" in acidic["soil_amendment"]

    alkaline = agronomic_engine.calculate_dosage(
        crop="Cotton", nitrogen=250, phosphorus=20, potassium=250, soil_ph=8.6, area_hectares=1.0
    )
    assert alkaline["soil_amendment"] is not None
    assert "Gypsum" in alkaline["soil_amendment"]


def test_fertilizer_predictor_inference():
    """Test ML formulation predictor and combined agronomic output."""
    res = fertilizer_predictor.recommend(
        crop="Paddy (Rice)",
        nitrogen=210.0,
        phosphorus=12.0,
        potassium=180.0,
        soil_ph=7.0,
        soil_type="Black Cotton",
        area_acres=4.0,
    )
    assert "recommended_blend" in res
    assert res["ml_confidence_pct"] >= 50.0
    assert res["farm_area_acres"] == 4.0
    assert res["total_50kg_bags"] > 0
    assert len(res["fertilizer_products"]) >= 3


def test_prediction_service_recommend_fertilizer():
    """Test service method and schema conversion."""
    req = FertilizerSupportRequest(
        crop="Chillies",
        district="Guntur",
        nitrogen=250.0,
        phosphorus=18.0,
        potassium=190.0,
        soil_ph=7.4,
        soil_type="Black Cotton",
        farm_area_acres=3.0,
    )
    res = prediction_service.recommend_fertilizer(req)
    assert res.crop == "Chillies"
    assert res.recommended_blend is not None
    assert len(res.recommended_fertilizers) >= 3
    assert len(res.application_schedule) >= 1
    assert "ANGRAU" in res.advisory_disclaimer


def test_api_fertilizer_endpoint():
    """Test FastAPI REST endpoint /api/v1/predict/fertilizer."""
    payload = {
        "crop": "Cotton",
        "district": "Guntur",
        "nitrogen": 230.0,
        "phosphorus": 14.0,
        "potassium": 210.0,
        "soil_ph": 7.3,
        "soil_type": "Black Cotton",
        "farm_area_acres": 5.0,
    }
    resp = client.post("/api/v1/predict/fertilizer", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["crop"] == "Cotton"
    assert "recommended_blend" in data
    assert "fertilizer_products" in data
    assert len(data["fertilizer_products"]) >= 3
    assert data["total_50kg_bags"] > 0
