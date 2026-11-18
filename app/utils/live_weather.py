"""
AgriAI Frontend - Real-Time Live Weather Client
Fetches and caches live meteorological telemetry and 5-day forecasts
via the AgriAI backend or direct Open-Meteo integration.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import streamlit as st
import requests
import logging

from app.utils.api_client import api_client

logger = logging.getLogger("agriai.frontend_weather")

AP_DISTRICT_COORDS: Dict[str, Dict[str, float]] = {
    "Guntur": {"lat": 16.3067, "lon": 80.4365},
    "Krishna": {"lat": 16.1875, "lon": 81.1389},
    "Vijayawada": {"lat": 16.5062, "lon": 80.6480},
    "Kurnool": {"lat": 15.8281, "lon": 78.0373},
    "Anantapur": {"lat": 14.6819, "lon": 77.6006},
    "East Godavari": {"lat": 16.9891, "lon": 82.2475},
    "Kakinada": {"lat": 16.9891, "lon": 82.2475},
    "Rajahmundry": {"lat": 17.0005, "lon": 81.8040},
    "West Godavari": {"lat": 16.7107, "lon": 81.0952},
    "Eluru": {"lat": 16.7107, "lon": 81.0952},
    "Visakhapatnam": {"lat": 17.6868, "lon": 83.2185},
    "Chittoor": {"lat": 13.2172, "lon": 79.1003},
    "Tirupati": {"lat": 13.6288, "lon": 79.4192},
    "Prakasam": {"lat": 15.5057, "lon": 80.0499},
    "Ongole": {"lat": 15.5057, "lon": 80.0499},
    "Nellore": {"lat": 14.4426, "lon": 79.9865},
    "YSR Kadapa": {"lat": 14.4673, "lon": 78.8242},
    "Kadapa": {"lat": 14.4673, "lon": 78.8242},
    "Srikakulam": {"lat": 18.2949, "lon": 83.8938},
    "Vizianagaram": {"lat": 18.1067, "lon": 83.3956},
    "Nandyal": {"lat": 15.4886, "lon": 78.4839},
    "Bapatla": {"lat": 15.9042, "lon": 80.4674},
    "Palnadu": {"lat": 16.2945, "lon": 79.9723},
    "Konaseema": {"lat": 16.5828, "lon": 82.0000},
    "Anakapalli": {"lat": 17.6913, "lon": 83.0039},
    "Sri Sathya Sai": {"lat": 14.1672, "lon": 77.8105},
}

WMO_ICONS: Dict[int, Dict[str, str]] = {
    0: {"condition": "Sunny / Clear", "icon": "☀️"},
    1: {"condition": "Mainly Clear", "icon": "🌤️"},
    2: {"condition": "Partly Cloudy", "icon": "⛅"},
    3: {"condition": "Overcast", "icon": "☁️"},
    45: {"condition": "Foggy", "icon": "🌫️"},
    48: {"condition": "Rime Fog", "icon": "🌫️"},
    51: {"condition": "Light Drizzle", "icon": "🌦️"},
    53: {"condition": "Moderate Drizzle", "icon": "🌦️"},
    55: {"condition": "Dense Drizzle", "icon": "🌧️"},
    61: {"condition": "Slight Rain", "icon": "🌧️"},
    63: {"condition": "Moderate Rain", "icon": "🌧️"},
    65: {"condition": "Heavy Rain", "icon": "⛈️"},
    80: {"condition": "Rain Showers", "icon": "🌦️"},
    81: {"condition": "Moderate Showers", "icon": "🌧️"},
    82: {"condition": "Violent Showers", "icon": "⛈️"},
    95: {"condition": "Thunderstorm", "icon": "⚡"},
    96: {"condition": "Thunderstorm w/ Hail", "icon": "⛈️"},
}


@st.cache_data(ttl=600, show_spinner=False)
def get_live_weather(district: str = "Guntur") -> Dict[str, Any]:
    """
    Fetch live weather telemetry for an AP district with caching.
    Tries backend service first, then direct Open-Meteo fallback.
    """
    clean_dist = district.strip() if district else "Guntur"
    if clean_dist.lower() in ["all", "andhra pradesh", ""]:
        clean_dist = "Guntur"

    # 1. Try Backend Live Weather Endpoint
    try:
        backend_data = api_client.get_live_weather(clean_dist)
        if backend_data and "temp_c" in backend_data:
            return backend_data
    except Exception as exc:
        logger.debug(f"Backend live weather call skipped: {exc}")

    # 2. Direct Open-Meteo API fallback
    coords = AP_DISTRICT_COORDS.get(clean_dist, {"lat": 16.3067, "lon": 80.4365})
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m,precipitation",
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": "Asia/Kolkata",
        "forecast_days": 6,
    }

    try:
        resp = requests.get(url, params=params, timeout=4.0)
        if resp.status_code == 200:
            payload = resp.json()
            cur = payload.get("current", {})
            daily = payload.get("daily", {})

            wcode = int(cur.get("weather_code", 2))
            wmo_meta = WMO_ICONS.get(wcode, {"condition": "Partly Cloudy", "icon": "🌤️"})

            # Parse daily forecast
            dates = daily.get("time", [])
            max_t = daily.get("temperature_2m_max", [])
            min_t = daily.get("temperature_2m_min", [])
            codes = daily.get("weather_code", [])

            forecast_days = []
            for i in range(len(dates)):
                dt_str = dates[i]
                try:
                    dt = datetime.strptime(dt_str, "%Y-%m-%d")
                    day_label = dt.strftime("%a")
                except Exception:
                    day_label = f"Day {i+1}"

                c = int(codes[i]) if i < len(codes) else 2
                day_meta = WMO_ICONS.get(c, {"condition": "Partly Cloudy", "icon": "🌤️"})

                forecast_days.append({
                    "date": dt_str,
                    "day": day_label,
                    "temp_max": float(max_t[i]) if i < len(max_t) else 32.0,
                    "temp_min": float(min_t[i]) if i < len(min_t) else 22.0,
                    "condition": day_meta["condition"],
                    "icon": day_meta["icon"],
                })

            return {
                "district": clean_dist,
                "latitude": coords["lat"],
                "longitude": coords["lon"],
                "temp_c": float(cur.get("temperature_2m", 30.0)),
                "feels_like_c": float(cur.get("apparent_temperature", 32.0)),
                "condition": wmo_meta["condition"],
                "icon": wmo_meta["icon"],
                "humidity": float(cur.get("relative_humidity_2m", 58.0)),
                "wind_speed": float(cur.get("wind_speed_10m", 9.0)),
                "precipitation_mm": float(cur.get("precipitation", 0.0)),
                "is_live": True,
                "forecast": forecast_days,
                "updated_at": datetime.now().strftime("%I:%M %p IST"),
            }
    except Exception as exc:
        logger.warning(f"Direct Open-Meteo fallback error: {exc}")

    # 3. Baseline fallback
    return {
        "district": clean_dist,
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "temp_c": 31.0,
        "feels_like_c": 33.0,
        "condition": "Partly Cloudy",
        "icon": "⛅",
        "humidity": 60.0,
        "wind_speed": 10.0,
        "precipitation_mm": 0.0,
        "is_live": False,
        "forecast": [
            {"day": "Thu", "temp_max": 32.0, "temp_min": 22.0, "condition": "Partly Cloudy", "icon": "⛅"},
            {"day": "Fri", "temp_max": 33.0, "temp_min": 23.0, "condition": "Sunny", "icon": "☀️"},
            {"day": "Sat", "temp_max": 31.0, "temp_min": 21.0, "condition": "Overcast", "icon": "☁️"},
            {"day": "Sun", "temp_max": 30.0, "temp_min": 20.0, "condition": "Light Rain", "icon": "🌦️"},
            {"day": "Mon", "temp_max": 32.0, "temp_min": 21.0, "condition": "Mainly Clear", "icon": "🌤️"},
        ],
        "updated_at": datetime.now().strftime("%I:%M %p IST"),
    }
