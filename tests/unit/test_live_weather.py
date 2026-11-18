"""
Unit tests for AgriAI Live Weather Intelligence & Open-Meteo Integration.
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.services.weather_live_service import live_weather_service, AP_DISTRICT_COORDINATES
from app.utils.live_weather import get_live_weather


@pytest.fixture
def client():
    return TestClient(app)


def test_district_coordinates_exist():
    assert "Guntur" in AP_DISTRICT_COORDINATES
    assert "Krishna" in AP_DISTRICT_COORDINATES
    assert "Visakhapatnam" in AP_DISTRICT_COORDINATES
    assert "lat" in AP_DISTRICT_COORDINATES["Guntur"]
    assert "lon" in AP_DISTRICT_COORDINATES["Guntur"]


def test_live_weather_service_fetch():
    data = live_weather_service.fetch_live_weather("Guntur")
    assert data is not None
    assert data["district"] == "Guntur"
    assert "temp_c" in data
    assert isinstance(data["temp_c"], (int, float))
    assert "condition" in data
    assert "humidity" in data
    assert "wind_speed" in data
    assert "forecast" in data
    assert len(data["forecast"]) >= 5

    # Check forecast structure
    day1 = data["forecast"][0]
    assert "day" in day1
    assert "temp_max" in day1
    assert "temp_min" in day1
    assert "icon" in day1


def test_live_weather_service_caching():
    data1 = live_weather_service.fetch_live_weather("Krishna")
    data2 = live_weather_service.fetch_live_weather("Krishna")
    # Cached responses should be identical objects
    assert data1["district"] == data2["district"]
    assert data1["temp_c"] == data2["temp_c"]


def test_live_weather_api_endpoint(client):
    response = client.get("/api/v1/analytics/weather/live?district=Guntur")
    assert response.status_code == 200
    payload = response.json()
    assert payload["district"] == "Guntur"
    assert "temp_c" in payload
    assert "feels_like_c" in payload
    assert "condition" in payload
    assert "icon" in payload
    assert "forecast" in payload
    assert len(payload["forecast"]) >= 5


def test_frontend_live_weather_helper():
    res = get_live_weather("Visakhapatnam")
    assert res is not None
    assert res["district"] == "Visakhapatnam"
    assert "temp_c" in res
    assert "condition" in res
    assert "forecast" in res
