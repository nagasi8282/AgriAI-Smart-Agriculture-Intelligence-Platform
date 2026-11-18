"""
AgriAI - Live Meteorological Service
Fetches real-time, high-resolution weather and 6-day numerical forecasts
using Open-Meteo API for Andhra Pradesh districts.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime
import time
import requests
import logging

logger = logging.getLogger("agriai.weather_live")

# Accurate geo-coordinates for Andhra Pradesh districts & agricultural hubs
AP_DISTRICT_COORDINATES: Dict[str, Dict[str, float]] = {
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
    "Alluri Sitharama Raju": {"lat": 18.0688, "lon": 82.5312},
    "Parvathipuram Manyam": {"lat": 18.7797, "lon": 83.4286},
}

# Standard WMO Weather Interpretation Codes
WMO_CODE_MAP: Dict[int, Dict[str, str]] = {
    0: {"condition": "Clear Sky", "icon": "☀️"},
    1: {"condition": "Mainly Clear", "icon": "🌤️"},
    2: {"condition": "Partly Cloudy", "icon": "⛅"},
    3: {"condition": "Overcast", "icon": "☁️"},
    45: {"condition": "Foggy", "icon": "🌫️"},
    48: {"condition": "Depositing Rime Fog", "icon": "🌫️"},
    51: {"condition": "Light Drizzle", "icon": "🌦️"},
    53: {"condition": "Moderate Drizzle", "icon": "🌦️"},
    55: {"condition": "Dense Drizzle", "icon": "🌧️"},
    56: {"condition": "Freezing Drizzle", "icon": "🌧️"},
    57: {"condition": "Dense Freezing Drizzle", "icon": "🌧️"},
    61: {"condition": "Slight Rain", "icon": "🌧️"},
    63: {"condition": "Moderate Rain", "icon": "🌧️"},
    65: {"condition": "Heavy Rain", "icon": "⛈️"},
    66: {"condition": "Freezing Rain", "icon": "🌧️"},
    67: {"condition": "Heavy Freezing Rain", "icon": "⛈️"},
    71: {"condition": "Slight Snow", "icon": "🌨️"},
    73: {"condition": "Moderate Snow", "icon": "🌨️"},
    75: {"condition": "Heavy Snow", "icon": "❄️"},
    77: {"condition": "Snow Grains", "icon": "🌨️"},
    80: {"condition": "Rain Showers", "icon": "🌦️"},
    81: {"condition": "Moderate Showers", "icon": "🌧️"},
    82: {"condition": "Violent Showers", "icon": "⛈️"},
    85: {"condition": "Snow Showers", "icon": "🌨️"},
    86: {"condition": "Heavy Snow Showers", "icon": "❄️"},
    95: {"condition": "Thunderstorm", "icon": "⚡"},
    96: {"condition": "Thunderstorm with Hail", "icon": "⛈️"},
    99: {"condition": "Severe Thunderstorm", "icon": "⛈️"},
}

DEFAULT_WMO = {"condition": "Partly Cloudy", "icon": "🌤️"}


class LiveWeatherService:
    """Manages real-time weather polling and in-memory caching."""

    def __init__(self, cache_ttl_seconds: int = 600):
        self.cache_ttl = cache_ttl_seconds
        self._cache: Dict[str, Dict[str, Any]] = {}

    def _resolve_district(self, district: Optional[str]) -> str:
        if not district or district.strip().lower() in ["all", "andhra pradesh"]:
            return "Guntur"
        
        target = district.strip()
        for d in AP_DISTRICT_COORDINATES:
            if d.lower() == target.lower():
                return d
        return "Guntur"

    def fetch_live_weather(self, district: Optional[str] = "Guntur") -> Dict[str, Any]:
        """Fetch live meteorological conditions and 6-day daily forecast."""
        canonical_district = self._resolve_district(district)
        cache_key = canonical_district.lower()

        # Check in-memory cache
        now = time.time()
        if cache_key in self._cache:
            entry = self._cache[cache_key]
            if now - entry["cached_at"] < self.cache_ttl:
                return entry["data"]

        coords = AP_DISTRICT_COORDINATES[canonical_district]
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,wind_speed_10m",
            "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum",
            "timezone": "Asia/Kolkata",
            "forecast_days": 6,
        }

        try:
            resp = requests.get(url, params=params, timeout=4.5)
            if resp.status_code == 200:
                payload = resp.json()
                current = payload.get("current", {})
                daily = payload.get("daily", {})

                # Parse current conditions
                wcode = int(current.get("weather_code", 2))
                wmo_info = WMO_CODE_MAP.get(wcode, DEFAULT_WMO)

                temp_c = float(current.get("temperature_2m", 30.0))
                feels_like = float(current.get("apparent_temperature", temp_c))
                humidity = float(current.get("relative_humidity_2m", 60.0))
                wind_kmh = float(current.get("wind_speed_10m", 10.0))
                precip_mm = float(current.get("precipitation", 0.0))

                # Parse 5-day forecast (excluding or including today)
                forecast_list: List[Dict[str, Any]] = []
                dates = daily.get("time", [])
                max_temps = daily.get("temperature_2m_max", [])
                min_temps = daily.get("temperature_2m_min", [])
                daily_wcodes = daily.get("weather_code", [])
                daily_precips = daily.get("precipitation_sum", [])

                for i in range(len(dates)):
                    dt_str = dates[i]
                    try:
                        dt = datetime.strptime(dt_str, "%Y-%m-%d")
                        day_name = dt.strftime("%a")
                    except Exception:
                        day_name = f"D+{i}"

                    day_code = int(daily_wcodes[i]) if i < len(daily_wcodes) else 2
                    day_wmo = WMO_CODE_MAP.get(day_code, DEFAULT_WMO)

                    forecast_list.append({
                        "date": dt_str,
                        "day": day_name,
                        "temp_max": float(max_temps[i]) if i < len(max_temps) else temp_c + 2.0,
                        "temp_min": float(min_temps[i]) if i < len(min_temps) else temp_c - 6.0,
                        "condition": day_wmo["condition"],
                        "icon": day_wmo["icon"],
                        "precipitation_mm": float(daily_precips[i]) if i < len(daily_precips) else 0.0,
                    })

                result = {
                    "district": canonical_district,
                    "latitude": coords["lat"],
                    "longitude": coords["lon"],
                    "temp_c": temp_c,
                    "feels_like_c": feels_like,
                    "condition": wmo_info["condition"],
                    "icon": wmo_info["icon"],
                    "humidity": humidity,
                    "wind_speed": wind_kmh,
                    "precipitation_mm": precip_mm,
                    "is_live": True,
                    "forecast": forecast_list,
                    "updated_at": datetime.now().strftime("%I:%M %p IST"),
                }

                # Store in cache
                self._cache[cache_key] = {"cached_at": now, "data": result}
                return result

        except Exception as exc:
            logger.warning(f"Live weather API lookup failed for {canonical_district}: {exc}. Using baseline.")

        # Resilient fallback baseline
        fallback_result = {
            "district": canonical_district,
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "temp_c": 31.0,
            "feels_like_c": 33.0,
            "condition": "Partly Cloudy",
            "icon": "⛅",
            "humidity": 62.0,
            "wind_speed": 11.0,
            "precipitation_mm": 0.0,
            "is_live": False,
            "forecast": [
                {"date": "2026-11-19", "day": "Thu", "temp_max": 32.0, "temp_min": 22.0, "condition": "Partly Cloudy", "icon": "⛅", "precipitation_mm": 0.0},
                {"date": "2026-11-20", "day": "Fri", "temp_max": 33.0, "temp_min": 23.0, "condition": "Sunny", "icon": "☀️", "precipitation_mm": 0.0},
                {"date": "2026-11-21", "day": "Sat", "temp_max": 31.0, "temp_min": 21.0, "condition": "Overcast", "icon": "☁️", "precipitation_mm": 0.5},
                {"date": "2026-11-22", "day": "Sun", "temp_max": 30.0, "temp_min": 20.0, "condition": "Light Rain", "icon": "🌦️", "precipitation_mm": 2.0},
                {"date": "2026-11-23", "day": "Mon", "temp_max": 32.0, "temp_min": 21.0, "condition": "Mainly Clear", "icon": "🌤️", "precipitation_mm": 0.0},
            ],
            "updated_at": datetime.now().strftime("%I:%M %p IST"),
        }
        return fallback_result


# Singleton service instance
live_weather_service = LiveWeatherService(cache_ttl_seconds=600)
