# AgriAI Sample Datasets (Andhra Pradesh)

This directory contains deterministic, validated baseline datasets representing the agricultural landscape of **Andhra Pradesh, India**. These files enable offline development, unit testing, and full local application demonstration without external API keys or cloud database requirements.

## Files Included

1. `crop_production_ap_sample.csv` (819 records)
   - Source: Directorate of Economics & Statistics (DES) / data.gov.in format
   - Coverage: 13 districts (Guntur, Krishna, Kurnool, Anantapur, East Godavari, etc.), Years 2015–2023
   - Target Crops: Paddy (Rice), Cotton, Chillies, Groundnut, Maize, Bengal Gram, Sugarcane
   - Columns: `state_name`, `district_name`, `crop_year`, `season`, `crop`, `area_hectares`, `production_tonnes`, `yield_quintal_per_ha`

2. `mandi_prices_ap_sample.csv` (1560 records)
   - Source: AGMARKNET (Agricultural Marketing Information Network) format
   - Coverage: Major AP mandis (Guntur APMC, Kurnool APMC, Vijayawada Market, Adoni Mandi, Tirupati Mandi, Rajahmundry Yard)
   - Period: Jan 2024 – Apr 2024
   - Columns: `state`, `district`, `market`, `commodity`, `variety`, `arrival_date`, `min_price_inr`, `max_price_inr`, `modal_price_inr`, `arrival_tonnes`

3. `weather_ap_sample.csv` (1573 records)
   - Source: IMD / Open-Meteo format
   - Coverage: Daily meteorological indicators across 13 AP districts
   - Period: Jan 2024 – Apr 2024
   - Columns: `state`, `district`, `date`, `temp_max_c`, `temp_min_c`, `temp_mean_c`, `rainfall_mm`, `relative_humidity_pct`, `wind_speed_kmh`, `is_forecast`, `condition`

4. `soil_health_ap_sample.csv` (13 records)
   - Source: Soil Health Card Portal
   - Coverage: Agro-ecological soil profiles for all 13 districts of AP
   - Columns: `state`, `district`, `soil_type`, `available_nitrogen_kg_ha`, `available_phosphorus_kg_ha`, `available_potassium_kg_ha`, `soil_ph`, `organic_carbon_pct`, `electrical_conductivity_dsm`, `nitrogen_category`, `phosphorus_category`, `potassium_category`

All data can be regenerated anytime using:
```powershell
python scripts\generate_sample_data.py
```
