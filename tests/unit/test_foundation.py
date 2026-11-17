"""
AgriAI Test Suite - Phase 1 Foundation & Core Verification Tests
Validates configuration, REST API endpoints, analytics, prediction services,
vision diagnostic pipeline, and AgriDoc AI RAG citation engine.
"""

import io
import pytest
from fastapi.testclient import TestClient
from PIL import Image

from backend.main import app
from backend.config.settings import settings
from backend.services.analytics_service import analytics_service
from backend.services.prediction_service import prediction_service
from backend.services.disease_service import disease_service
from backend.services.rag_service import rag_service
from storage.local_storage import local_storage

client = TestClient(app)


# ------------------------------------------------------------------------------
# 1. Configuration & Settings Tests
# ------------------------------------------------------------------------------
def test_settings_initialization():
    """Verify application configuration loads default parameters correctly."""
    assert settings.DEFAULT_STATE == "Andhra Pradesh"
    assert "Guntur" in settings.district_list
    assert len(settings.district_list) >= 10
    assert settings.VERSION == "1.0.0"


# ------------------------------------------------------------------------------
# 2. Health & Diagnostics Endpoints
# ------------------------------------------------------------------------------
def test_health_check_endpoints():
    """Verify both /health and /api/v1/health return HTTP 200 and healthy status."""
    for path in ["/health", f"{settings.API_V1_STR}/health"]:
        response = client.get(path)
        assert response.status_code == 200
        payload = response.json()
        assert payload["status"] == "healthy"
        assert payload["app_name"] == settings.PROJECT_NAME
        assert "storage_layer" in payload["services"]


def test_root_discovery_endpoint():
    """Verify root API returns service links and target region."""
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["target_region"] == "Andhra Pradesh"
    assert "docs_url" in payload


# ------------------------------------------------------------------------------
# 3. Analytics Service & Endpoints
# ------------------------------------------------------------------------------
def test_dashboard_summary():
    """Verify dashboard KPI summary computation."""
    summary = analytics_service.get_dashboard_summary()
    assert summary.total_crop_records > 0
    assert summary.total_districts >= 10
    assert summary.total_crops_tracked >= 5


def test_crop_production_filtering():
    """Verify crop production filtering by district and crop."""
    response = client.get(f"{settings.API_V1_STR}/analytics/crops?district=Guntur&crop=Paddy (Rice)")
    assert response.status_code == 200
    records = response.json()
    assert len(records) > 0
    for r in records:
        assert r["district_name"] == "Guntur"
        assert "Paddy" in r["crop"]
        assert r["yield_quintal_per_ha"] > 0


def test_mandi_prices_endpoint():
    """Verify AGMARKNET mandi prices endpoint."""
    response = client.get(f"{settings.API_V1_STR}/analytics/mandi-prices?commodity=Chillies")
    assert response.status_code == 200
    records = response.json()
    assert len(records) > 0
    first = records[0]
    assert first["min_price_inr"] <= first["modal_price_inr"] <= first["max_price_inr"]


def test_weather_endpoint():
    """Verify meteorological records endpoint."""
    response = client.get(f"{settings.API_V1_STR}/analytics/weather?district=Kurnool")
    assert response.status_code == 200
    records = response.json()
    assert len(records) > 0
    assert records[0]["temp_max_c"] >= records[0]["temp_min_c"]


def test_soil_endpoint():
    """Verify soil health profiles endpoint."""
    response = client.get(f"{settings.API_V1_STR}/analytics/soil?district=Guntur")
    assert response.status_code == 200
    records = response.json()
    assert len(records) == 1
    assert records[0]["soil_type"] == "Black Cotton"
    assert 5.0 <= records[0]["soil_ph"] <= 9.0


# ------------------------------------------------------------------------------
# 4. Machine Learning & Prediction Endpoints
# ------------------------------------------------------------------------------
def test_yield_prediction():
    """Verify ML crop yield estimation and TreeSHAP feature attributions."""
    payload = {
        "state": "Andhra Pradesh",
        "district": "Guntur",
        "crop": "Paddy (Rice)",
        "season": "Kharif",
        "crop_year": 2024,
        "area_hectares": 10.0,
        "rainfall_mm": 900.0,
        "temp_avg_c": 28.5,
        "soil_ph": 7.2,
        "nitrogen_kg_ha": 320.0,
        "phosphorus_kg_ha": 24.0,
        "potassium_kg_ha": 190.0,
    }
    response = client.post(f"{settings.API_V1_STR}/predict/yield", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_yield_quintal_per_ha"] > 0
    assert data["estimated_total_production_tonnes"] > 0
    assert "feature_importance" in data
    assert "TreeSHAP" in data["model_algorithm"]


def test_mandi_price_prediction():
    """Verify time-series mandi price forecast."""
    payload = {
        "state": "Andhra Pradesh",
        "district": "Guntur",
        "market": "Guntur APMC",
        "commodity": "Chillies",
        "forecast_horizon_days": 10,
    }
    response = client.post(f"{settings.API_V1_STR}/predict/price", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["predicted_modal_price"] > 0
    assert len(data["historical_price_trend"]) > 0


def test_fertilizer_support():
    """Verify transparent rule-based fertilizer scheduling."""
    payload = {
        "crop": "Paddy (Rice)",
        "district": "Guntur",
        "nitrogen": 210.0,  # Low
        "phosphorus": 14.0,  # Medium
        "potassium": 220.0,  # Medium
        "soil_ph": 7.2,
        "soil_type": "Black Cotton",
    }
    response = client.post(f"{settings.API_V1_STR}/predict/fertilizer", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "Deficient" in data["nutrient_status"]["Nitrogen (N)"]
    assert len(data["recommended_fertilizers"]) > 0
    assert len(data["application_schedule"]) == 3


# ------------------------------------------------------------------------------
# 5. Plant Foliage Disease Vision Endpoint
# ------------------------------------------------------------------------------
def test_disease_detection_with_valid_image():
    """Verify disease diagnosis returns predicted class, Grad-CAM heatmap, and disclaimers."""
    # Generate synthetic in-memory JPEG image
    img = Image.new("RGB", (256, 256), color=(45, 120, 45))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)

    files = {"file": ("test_leaf.jpg", buf.getvalue(), "image/jpeg")}
    data = {"crop_hint": "Tomato"}
    response = client.post(f"{settings.API_V1_STR}/disease/predict", files=files, data=data)

    assert response.status_code == 200
    res = response.json()
    assert res["is_valid_plant"] is True
    assert "Tomato" in res["crop_name"]
    assert res["confidence"] > 50.0
    assert res["gradcam_heatmap_base64"] is not None
    assert "CRITICAL ADVISORY" in res["disclaimer"]


# ------------------------------------------------------------------------------
# 6. AgriDoc AI PDF RAG & Citations
# ------------------------------------------------------------------------------
def test_agridoc_ai_query_with_citations():
    """Verify literature RAG returns grounded answer with page citations."""
    payload = {"query": "Which CNN architectures are compared in Demilie 2024?", "top_k": 2}
    response = client.post(f"{settings.API_V1_STR}/documents/ask", json=payload)

    assert response.status_code == 200
    res = response.json()
    assert res["grounded_in_documents"] is True
    assert len(res["citations"]) > 0
    first_cit = res["citations"][0]
    assert first_cit["page_number"] > 0
    assert "Demilie" in first_cit["document_name"]


def test_agridoc_ai_anti_hallucination():
    """Verify RAG refuses to fabricate answers when evidence is absent."""
    payload = {"query": "What is the quantum computing algorithm for interstellar wheat breeding?"}
    response = client.post(f"{settings.API_V1_STR}/documents/ask", json=payload)

    assert response.status_code == 200
    res = response.json()
    assert res["grounded_in_documents"] is False
    assert len(res["citations"]) == 0
    assert "could not find relevant supporting evidence" in res["answer"].lower()


# ------------------------------------------------------------------------------
# 7. Local Storage Layer
# ------------------------------------------------------------------------------
def test_local_storage_checksum():
    """Verify cryptographic checksum computation."""
    import tempfile
    from pathlib import Path

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(b"AgriAI Data Engineering Test Payload")
        tmp_path = Path(tmp.name)

    checksum = local_storage.compute_checksum(tmp_path)
    assert len(checksum) == 64
    tmp_path.unlink()
