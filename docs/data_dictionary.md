# AgriAI: Medallion Data Dictionary & Schema Specifications

## 1. Overview & Architecture Conformance
This document specifies the technical metadata, column definitions, data types, primary/foreign key constraints, and business rules governing the **Silver (Conformed)** and **Gold (Dimensional Marts)** layers of the AgriAI Data Warehouse.

---

## 2. Silver Layer (Conformed & Staging Tables)

### 2.1 `silver_crop_production`
- **Description**: Cleaned, standardized, and conformed crop area and harvest production records.
- **Grain**: One record per District, Agricultural Year, Season, and Crop.

| Column Name | Data Type | Nullable | Constraint | Description | Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | INTEGER | No | PK, Auto | Surrogate staging identifier | `101` |
| `state` | VARCHAR(50) | No | Default 'AP' | State of India | `Andhra Pradesh` |
| `district` | VARCHAR(100) | No | Indexed | Standardized Census district name | `Guntur` |
| `crop_year` | INTEGER | No | Indexed | Agricultural year (e.g., 2023 for 2023-24) | `2023` |
| `season` | VARCHAR(50) | No | Enum | Growing season (`Kharif`, `Rabi`, `Summer`, `Whole Year`) | `Kharif` |
| `crop` | VARCHAR(100) | No | Indexed | Standardized botanical/trade crop name | `Paddy (Rice)` |
| `area_hectares` | FLOAT | No | Check $> 0$ | Cultivated land area in hectares | `124500.50` |
| `production_tonnes` | FLOAT | No | Check $\ge 0$ | Total metric production in tonnes | `485550.00` |
| `yield_quintal_per_ha` | FLOAT | No | Check $> 0$ | Harvest yield in quintals per hectare | `39.00` |
| `_checksum` | VARCHAR(64) | No | Unique Index | SHA-256 fingerprint for deduplication audit | `a3b8...` |
| `_ingested_at` | TIMESTAMP | No | Auto UTC | Timestamp of Silver transformation load | `2024-05-01 10:30:00` |

---

### 2.2 `silver_mandi_prices`
- **Description**: Cleaned AGMARKNET daily wholesale commodity spot transactions.
- **Grain**: One record per Market Yard, Commodity, Variety, and Trading Date.

| Column Name | Data Type | Nullable | Constraint | Description | Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | INTEGER | No | PK, Auto | Surrogate staging identifier | `501` |
| `state` | VARCHAR(50) | No | Default 'AP' | State of India | `Andhra Pradesh` |
| `district` | VARCHAR(100) | No | Indexed | District hosting the APMC yard | `Guntur` |
| `market` | VARCHAR(150) | No | Indexed | Official APMC Market yard name | `Guntur APMC` |
| `commodity` | VARCHAR(100) | No | Indexed | Standardized agricultural commodity | `Chillies` |
| `variety` | VARCHAR(100) | Yes | Default 'FAQ' | Commercial variety or grade classification | `Standard/FAQ` |
| `arrival_date` | DATE | No | Indexed | Date of wholesale trading session | `2024-04-15` |
| `min_price_inr` | FLOAT | No | Check $> 0$ | Minimum transaction price (₹/Quintal) | `17500.00` |
| `max_price_inr` | FLOAT | No | Check $\ge$ Min | Maximum transaction price (₹/Quintal) | `21000.00` |
| `modal_price_inr` | FLOAT | No | Check Band | Most frequent transaction price (₹/Quintal) | `19200.00` |
| `arrival_tonnes` | FLOAT | Yes | Default 0.0 | Daily commodity arrival quantity in tonnes | `120.50` |
| `_checksum` | VARCHAR(64) | No | Unique Index | SHA-256 fingerprint | `f7c1...` |
| `_ingested_at` | TIMESTAMP | No | Auto UTC | Timestamp of Silver transformation load | `2024-05-01 10:30:00` |

---

### 2.3 `silver_weather`
- **Description**: Standardized daily meteorological observations and numerical forecasts.
- **Grain**: One record per District and Calendar Date.

| Column Name | Data Type | Nullable | Constraint | Description | Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | INTEGER | No | PK, Auto | Surrogate staging identifier | `301` |
| `district` | VARCHAR(100) | No | Indexed | Andhra Pradesh district name | `Kurnool` |
| `observation_date` | DATE | No | Indexed | Date of observation | `2024-04-15` |
| `temp_max_c` | FLOAT | No | Check $\ge$ Min | Daily maximum ambient temperature (°C) | `38.5` |
| `temp_min_c` | FLOAT | No | Check | Daily minimum ambient temperature (°C) | `24.0` |
| `temp_mean_c` | FLOAT | No | Check | Mean daily ambient temperature (°C) | `31.25` |
| `rainfall_mm` | FLOAT | No | Check $\ge 0$ | 24-hour cumulative rainfall (mm) | `12.5` |
| `relative_humidity_pct` | FLOAT | No | Check $[0, 100]$ | Daily average relative humidity (%) | `68.0` |
| `wind_speed_kmh` | FLOAT | No | Check $\ge 0$ | Average wind velocity (km/h) | `14.2` |
| `is_forecast` | BOOLEAN | No | Default False | Flag: False = Observed, True = Forecast | `False` |
| `condition` | VARCHAR(50) | Yes | Default 'Normal' | Weather sky condition descriptor | `Partly Cloudy` |
| `_checksum` | VARCHAR(64) | No | Unique Index | SHA-256 fingerprint | `e4d9...` |
| `_ingested_at` | TIMESTAMP | No | Auto UTC | Timestamp of Silver transformation load | `2024-05-01 10:30:00` |

---

### 2.4 `silver_soil`
- **Description**: Standardized Soil Health Card district nutrient indices.
- **Grain**: One record per District.

| Column Name | Data Type | Nullable | Constraint | Description | Example |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `id` | INTEGER | No | PK, Auto | Surrogate staging identifier | `12` |
| `district` | VARCHAR(100) | No | Unique Index | Andhra Pradesh district name | `Guntur` |
| `soil_type` | VARCHAR(100) | No | Standardized | Primary soil classification | `Black Cotton` |
| `available_nitrogen_kg_ha` | FLOAT | No | Check $\ge 0$ | Available soil Nitrogen in kg/ha | `265.0` |
| `available_phosphorus_kg_ha` | FLOAT | No | Check $\ge 0$ | Available soil Phosphorus in kg/ha | `18.5` |
| `available_potassium_kg_ha` | FLOAT | No | Check $\ge 0$ | Available soil Potassium in kg/ha | `210.0` |
| `soil_ph` | FLOAT | No | Check $[3.5, 10.5]$ | Soil acidity/alkalinity scale | `7.2` |
| `organic_carbon_pct` | FLOAT | No | Check $\ge 0$ | Organic Carbon content percentage | `0.65` |
| `electrical_conductivity_dsm` | FLOAT | No | Check $\ge 0$ | Salinity measure (dS/m) | `0.45` |
| `nitrogen_category` | VARCHAR(20) | Yes | Enum | Rating (`Low`, `Medium`, `High`) | `Low` |
| `phosphorus_category` | VARCHAR(20) | Yes | Enum | Rating (`Low`, `Medium`, `High`) | `Medium` |
| `potassium_category` | VARCHAR(20) | Yes | Enum | Rating (`Low`, `Medium`, `High`) | `Medium` |

---

## 3. Gold Layer (Dimensional Star Schema)

### 3.1 Dimensions

#### `gold_dim_date`
- **Grain**: One record per calendar day.
- **Columns**: `date_id` (INT, PK, e.g. `20240415`), `calendar_date` (DATE, Unique), `year` (INT), `month` (INT), `month_name` (VARCHAR), `quarter` (INT), `season` (VARCHAR).

#### `gold_dim_location`
- **Grain**: One record per administrative district in Andhra Pradesh.
- **Columns**: `location_id` (INT, PK, Auto), `state` (VARCHAR), `district` (VARCHAR, Unique), `agro_climatic_zone` (VARCHAR), `latitude` (FLOAT), `longitude` (FLOAT).

#### `gold_dim_crop`
- **Grain**: One record per botanical crop variety.
- **Columns**: `crop_id` (INT, PK, Auto), `crop_name` (VARCHAR, Unique), `crop_category` (VARCHAR, e.g. `Commercial`, `Foodgrain`, `Oilseed`), `botanical_name` (VARCHAR), `major_growing_season` (VARCHAR).

#### `gold_dim_market`
- **Grain**: One record per regulated APMC market yard.
- **Columns**: `market_id` (INT, PK, Auto), `market_name` (VARCHAR, Unique), `district` (VARCHAR), `apmc_code` (VARCHAR).

---

### 3.2 Fact Marts

#### `gold_fact_crop_production`
- **Grain**: One record per `date_id`, `location_id`, and `crop_id`.
- **Columns**: `production_id` (INT, PK), `date_id` (INT, FK), `location_id` (INT, FK), `crop_id` (INT, FK), `area_hectares` (FLOAT), `production_tonnes` (FLOAT), `yield_quintal_per_ha` (FLOAT).

#### `gold_fact_mandi_price`
- **Grain**: One record per `date_id`, `location_id`, `crop_id`, and `market_id`.
- **Columns**: `mandi_price_id` (INT, PK), `date_id` (INT, FK), `location_id` (INT, FK), `crop_id` (INT, FK), `market_id` (INT, FK), `min_price_inr` (FLOAT), `max_price_inr` (FLOAT), `modal_price_inr` (FLOAT), `arrival_tonnes` (FLOAT).

#### `gold_fact_weather`
- **Grain**: One record per `date_id` and `location_id`.
- **Columns**: `weather_id` (INT, PK), `date_id` (INT, FK), `location_id` (INT, FK), `temp_max_c` (FLOAT), `temp_min_c` (FLOAT), `temp_mean_c` (FLOAT), `rainfall_mm` (FLOAT), `relative_humidity_pct` (FLOAT), `wind_speed_kmh` (FLOAT).

#### `gold_fact_soil`
- **Grain**: One record per `location_id`.
- **Columns**: `soil_id` (INT, PK), `location_id` (INT, FK, Unique), `nitrogen_kg_ha` (FLOAT), `phosphorus_kg_ha` (FLOAT), `potassium_kg_ha` (FLOAT), `soil_ph` (FLOAT), `organic_carbon_pct` (FLOAT), `electrical_conductivity_dsm` (FLOAT), `soil_type` (VARCHAR).
