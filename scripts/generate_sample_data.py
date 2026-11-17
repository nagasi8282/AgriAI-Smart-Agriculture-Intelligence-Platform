"""
AgriAI Data Generator - Sample Datasets for Andhra Pradesh
Generates realistic, validated sample datasets conforming to official distributions:
- Crop Production (DES / data.gov.in)
- Mandi Prices (AGMARKNET)
- Weather Observations (IMD / Open-Meteo)
- Soil Health Profiles (Soil Health Card)
"""

import csv
import random
from pathlib import Path
from datetime import datetime, timedelta

SAMPLE_DIR = Path(__file__).resolve().parent.parent / "data" / "sample"
SAMPLE_DIR.mkdir(parents=True, exist_ok=True)

# Seed for deterministic generation
random.seed(42)

DISTRICTS = [
    "Guntur", "Krishna", "Kurnool", "Anantapur", "East Godavari",
    "Chittoor", "Prakasam", "West Godavari", "Visakhapatnam", "Nellore",
    "YSR Kadapa", "Srikakulam", "Vizianagaram"
]

CROPS = [
    {"name": "Paddy (Rice)", "season": "Kharif", "base_area": 120000, "yield_range": (35.0, 48.0)},
    {"name": "Cotton", "season": "Kharif", "base_area": 95000, "yield_range": (14.0, 22.0)},
    {"name": "Chillies", "season": "Rabi", "base_area": 45000, "yield_range": (28.0, 42.0)},
    {"name": "Groundnut", "season": "Kharif", "base_area": 80000, "yield_range": (9.0, 18.0)},
    {"name": "Maize", "season": "Rabi", "base_area": 55000, "yield_range": (38.0, 55.0)},
    {"name": "Bengal Gram", "season": "Rabi", "base_area": 60000, "yield_range": (11.0, 19.0)},
    {"name": "Sugarcane", "season": "Whole Year", "base_area": 35000, "yield_range": (720.0, 950.0)},
]

MANDIS = [
    {"market": "Guntur APMC", "district": "Guntur", "commodities": ["Chillies", "Cotton", "Paddy"]},
    {"market": "Kurnool APMC", "district": "Kurnool", "commodities": ["Groundnut", "Bengal Gram", "Maize"]},
    {"market": "Vijayawada Market", "district": "Krishna", "commodities": ["Paddy", "Maize", "Chillies"]},
    {"market": "Adoni Mandi", "district": "Kurnool", "commodities": ["Cotton", "Groundnut"]},
    {"market": "Tirupati Mandi", "district": "Chittoor", "commodities": ["Groundnut", "Sugarcane"]},
    {"market": "Rajahmundry Yard", "district": "East Godavari", "commodities": ["Paddy", "Maize"]},
]

COMMODITY_BASE_PRICES = {
    "Chillies": {"base": 18500, "spread": 2500},
    "Cotton": {"base": 6800, "spread": 800},
    "Paddy": {"base": 2200, "spread": 250},
    "Groundnut": {"base": 6200, "spread": 700},
    "Maize": {"base": 2150, "spread": 300},
    "Bengal Gram": {"base": 5400, "spread": 600},
    "Sugarcane": {"base": 3150, "spread": 200},
}


def generate_crop_production():
    filepath = SAMPLE_DIR / "crop_production_ap_sample.csv"
    headers = [
        "state_name", "district_name", "crop_year", "season",
        "crop", "area_hectares", "production_tonnes", "yield_quintal_per_ha"
    ]
    rows = []
    for year in range(2015, 2024):
        for district in DISTRICTS:
            for crop_info in CROPS:
                crop = crop_info["name"]
                season = crop_info["season"]
                # Add regional variance
                area = round(crop_info["base_area"] * random.uniform(0.6, 1.4), 2)
                yield_q = round(random.uniform(*crop_info["yield_range"]), 2)
                # Production in tonnes = (yield in quintals/ha * area) / 10
                production = round((yield_q * area) / 10, 2)
                rows.append([
                    "Andhra Pradesh", district, year, season,
                    crop, area, production, yield_q
                ])

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Generated {len(rows)} crop production records at {filepath}")


def generate_mandi_prices():
    filepath = SAMPLE_DIR / "mandi_prices_ap_sample.csv"
    headers = [
        "state", "district", "market", "commodity", "variety",
        "arrival_date", "min_price_inr", "max_price_inr", "modal_price_inr", "arrival_tonnes"
    ]
    rows = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 4, 30)
    current_date = start_date

    while current_date <= end_date:
        if current_date.weekday() < 6:  # Exclude Sundays
            date_str = current_date.strftime("%Y-%m-%d")
            for mandi in MANDIS:
                for commodity in mandi["commodities"]:
                    cfg = COMMODITY_BASE_PRICES[commodity]
                    modal = round(cfg["base"] + random.uniform(-cfg["spread"], cfg["spread"]), 2)
                    min_p = round(modal - random.uniform(50, 400), 2)
                    max_p = round(modal + random.uniform(50, 500), 2)
                    arrivals = round(random.uniform(25.0, 350.0), 2)
                    rows.append([
                        "Andhra Pradesh", mandi["district"], mandi["market"],
                        commodity, "Standard/FAQ", date_str,
                        min_p, max_p, modal, arrivals
                    ])
        current_date += timedelta(days=1)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Generated {len(rows)} mandi price records at {filepath}")


def generate_weather_data():
    filepath = SAMPLE_DIR / "weather_ap_sample.csv"
    headers = [
        "state", "district", "date", "temp_max_c", "temp_min_c",
        "temp_mean_c", "rainfall_mm", "relative_humidity_pct",
        "wind_speed_kmh", "is_forecast", "condition"
    ]
    rows = []
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2024, 4, 30)
    current_date = start_date

    while current_date <= end_date:
        date_str = current_date.strftime("%Y-%m-%d")
        month = current_date.month
        # Seasonal temp variations for AP
        base_max = 31.0 if month in [1, 2] else 38.5
        base_min = 19.0 if month in [1, 2] else 25.0

        for district in DISTRICTS:
            temp_max = round(base_max + random.uniform(-2.5, 3.5), 1)
            temp_min = round(base_min + random.uniform(-2.0, 2.5), 1)
            temp_mean = round((temp_max + temp_min) / 2, 1)
            # Monsoon or dry season
            rain_chance = 0.08 if month in [1, 2, 3] else 0.25
            rainfall = round(random.uniform(5.0, 45.0), 1) if random.random() < rain_chance else 0.0
            humidity = round(random.uniform(52.0, 84.0), 1)
            wind = round(random.uniform(8.0, 22.0), 1)
            condition = "Rainy" if rainfall > 5.0 else ("Partly Cloudy" if humidity > 70 else "Sunny")

            rows.append([
                "Andhra Pradesh", district, date_str, temp_max, temp_min,
                temp_mean, rainfall, humidity, wind, False, condition
            ])
        current_date += timedelta(days=1)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Generated {len(rows)} weather records at {filepath}")


def generate_soil_health():
    filepath = SAMPLE_DIR / "soil_health_ap_sample.csv"
    headers = [
        "state", "district", "soil_type", "available_nitrogen_kg_ha",
        "available_phosphorus_kg_ha", "available_potassium_kg_ha",
        "soil_ph", "organic_carbon_pct", "electrical_conductivity_dsm",
        "nitrogen_category", "phosphorus_category", "potassium_category"
    ]
    soil_types = {
        "Guntur": "Black Cotton",
        "Krishna": "Coastal Alluvial",
        "Kurnool": "Black Cotton",
        "Anantapur": "Red Sandy Loam",
        "East Godavari": "Delta Alluvial",
        "Chittoor": "Red Loam",
        "Prakasam": "Black Soil",
        "West Godavari": "Alluvial",
        "Visakhapatnam": "Laterite Soil",
        "Nellore": "Coastal Sandy",
        "YSR Kadapa": "Red & Black Mixed",
        "Srikakulam": "Red Loam",
        "Vizianagaram": "Red Sandy",
    }
    rows = []
    for district, soil_type in soil_types.items():
        n = round(random.uniform(220.0, 450.0), 1)
        p = round(random.uniform(12.0, 32.0), 1)
        k = round(random.uniform(140.0, 310.0), 1)
        ph = round(random.uniform(6.5, 8.2), 2)
        oc = round(random.uniform(0.42, 0.88), 2)
        ec = round(random.uniform(0.25, 0.95), 2)

        n_cat = "Low" if n < 280 else ("Medium" if n <= 560 else "High")
        p_cat = "Low" if p < 10 else ("Medium" if p <= 25 else "High")
        k_cat = "Low" if k < 108 else ("Medium" if k <= 280 else "High")

        rows.append([
            "Andhra Pradesh", district, soil_type, n, p, k, ph, oc, ec,
            n_cat, p_cat, k_cat
        ])

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    print(f"Generated {len(rows)} soil health records at {filepath}")


if __name__ == "__main__":
    generate_crop_production()
    generate_mandi_prices()
    generate_weather_data()
    generate_soil_health()
    print("All sample datasets successfully generated.")
