"""
AgriAI Test Suite - Deployment Integration & Standalone Module Tests
Validates that every single one of the 12 platform modules executes cleanly
in standalone zero-cost mode (direct in-process fallback without requiring an external HTTP server).
"""

import pytest
from app.utils.api_client import api_client
from app.utils.live_weather import get_live_weather


def test_standalone_health():
    """Verify health endpoint operates in standalone zero-cost mode."""
    health = api_client.get_health()
    assert health is not None
    assert health["status"] == "healthy"
    assert "services" in health


def test_standalone_dashboard_summary():
    """Verify dashboard KPI summary computes in-process."""
    summary = api_client.get_dashboard_summary()
    assert summary is not None
    assert "total_districts" in summary or "total_crop_records" in summary
    assert len(summary.get("districts_list", [])) > 0


def test_standalone_crop_intelligence():
    """Verify crop intelligence records retrieve and filter properly."""
    crops = api_client.get_crop_production(district="Guntur")
    assert isinstance(crops, list)
    assert len(crops) > 0
    first = crops[0]
    assert "crop" in first
    assert "production_tonnes" in first


def test_standalone_mandi_prices():
    """Verify mandi wholesale prices and arrivals retrieve properly."""
    mandi = api_client.get_mandi_prices(district="Guntur")
    assert isinstance(mandi, list)
    assert len(mandi) > 0
    assert "modal_price_inr" in mandi[0]


def test_standalone_live_weather():
    """Verify live meteorological telemetry and 5-day forecast."""
    weather = get_live_weather("Guntur")
    assert weather is not None
    assert weather["district"] == "Guntur"
    assert "temp_c" in weather
    assert "condition" in weather
    assert "forecast" in weather
    assert len(weather["forecast"]) >= 5


def test_standalone_soil_intelligence():
    """Verify soil health card ratings retrieve properly."""
    soil = api_client.get_soil(district="Guntur")
    assert isinstance(soil, list)
    assert len(soil) > 0
    assert "soil_ph" in soil[0]


def test_standalone_fertilizer_recommendation():
    """Verify fertilizer nutrient balance and bag calculation."""
    payload = {
        "crop": "Cotton",
        "district": "Guntur",
        "nitrogen": 180.0,
        "phosphorus": 14.0,
        "potassium": 280.0,
        "soil_ph": 7.2,
        "farm_area_acres": 2.5,
    }
    result = api_client.recommend_fertilizer(payload)
    assert "error" not in result
    assert "nutrient_status" in result
    assert "recommended_fertilizers" in result
    assert len(result["recommended_fertilizers"]) > 0


def test_standalone_yield_prediction():
    """Verify crop yield ML prediction."""
    payload = {
        "district": "Guntur",
        "crop": "Paddy (Rice)",
        "season": "Kharif",
        "area_hectares": 3.0,
        "annual_rainfall_mm": 950.0,
        "fertilizer_total_kg_ha": 150.0,
        "irrigation_ratio": 0.85,
    }
    res = api_client.predict_yield(payload)
    assert "error" not in res
    assert "predicted_yield_quintal_per_ha" in res
    assert res["predicted_yield_quintal_per_ha"] > 0


def test_standalone_price_prediction():
    """Verify mandi price forecasting ML."""
    payload = {
        "district": "Guntur",
        "market": "Guntur APMC",
        "commodity": "Chillies",
        "forecast_days": 14,
        "current_modal_price": 18500.0,
    }
    res = api_client.predict_price(payload)
    assert "error" not in res
    assert "predicted_modal_price" in res
    assert res["predicted_modal_price"] > 0


def test_standalone_disease_detection():
    """Verify computer vision foliage disease diagnosis."""
    from PIL import Image
    import io
    img = Image.new("RGB", (64, 64), color=(34, 139, 34))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    img_bytes = buf.getvalue()

    res = api_client.predict_disease(img_bytes, filename="leaf_test.jpg", crop_hint="Tomato")
    assert "error" not in res
    assert res.get("is_valid_plant") is True
    assert "predicted_class" in res
    assert "gradcam_heatmap_base64" in res


def test_standalone_agriai_chat():
    """Verify AgriAI grounding assistant chat response."""
    res = api_client.chat_assistant("What is the current mandi price of chillies in Guntur?", district="Guntur")
    assert res is not None
    assert "response" in res
    assert len(res["response"]) > 10


def test_standalone_agridoc_ai_rag():
    """Verify AgriDoc AI PDF question answering with page-level citations."""
    docs = api_client.list_documents()
    assert isinstance(docs, list)
    assert len(docs) > 0

    query_res = api_client.ask_document("What deep learning architectures are evaluated in plant disease research?")
    assert "answer" in query_res
    assert "citations" in query_res
    assert len(query_res["citations"]) > 0
    assert "page_number" in query_res["citations"][0]
