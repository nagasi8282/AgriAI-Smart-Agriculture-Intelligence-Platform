# AgriAI: Smart Agriculture Intelligence Platform
## Centralized Dataset Registry & Data Extraction Specifications

### 1. Master Dataset Catalog

| Domain | Source Name | Primary Publisher | Format | Update Frequency | License / Access Conditions | Ingestion Pattern |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Crop Production** | AP District-wise Crop Area & Production | Directorate of Economics and Statistics (DES) / data.gov.in | CSV / JSON | Annual / Seasonal | Open Government Data License (OGDL) India | Full & Periodic Incremental |
| **Mandi Market Prices** | AGMARKNET Daily Wholesale Commodity Prices | Directorate of Marketing & Inspection (DMI), MoA&FW | CSV / REST API | Daily (Trade days) | OGDL India / Public Domain | Incremental by `arrival_date` |
| **Weather (Observed & Forecast)** | Meteorological Time-Series & Forecasts | India Meteorological Department (IMD) / Open-Meteo Historical & Forecast API | JSON / CSV | Daily / Hourly | CC-BY 4.0 / Public Open Access | Scheduled Window Incremental |
| **Soil Health Indices** | Andhra Pradesh District-wise Soil Fertility | Department of Agriculture & Farmers Welfare / Soil Health Card Portal | CSV / XLSX | Periodic (Biennial Survey) | Official Government Report | Snapshot Full Load |
| **Foliage Disease Imagery** | New Plant Diseases Dataset (PlantVillage Extension) | Kaggle / Vipul Patel / Penn State University | JPEG Images | Static Benchmark | Public Domain / CC0 / Academic Use | Bulk Download / Local Import |
| **Agronomy Literature & Research** | Agricultural Research Papers & Bulletins | Journal of Big Data (Demilie, 2024) / ICAR / ANGRAU | PDF | On-Demand Upload | Creative Commons Attribution 4.0 (CC BY) | Multi-part Form Upload |

---

### 2. Domain-Specific Ingestion & Extraction Specifications

#### 2.1 Crop Production Ingestion Specification
- **Publisher**: Ministry of Agriculture & Farmers Welfare, Government of India.
- **Geographic Scope**: Andhra Pradesh (State Code: `AP`), covering 13 legacy / 26 reorganized districts:
  - Anantapur, Chittoor, East Godavari, Guntur, Krishna, Kurnool, Prakasam, Srikakulam, Visakhapatnam, Vizianagaram, West Godavari, YSR Kadapa, Nellore.
- **Key Target Crops**:
  - Cereals: Paddy (Rice), Maize, Jowar, Bajra
  - Commercial / Cash Crops: Cotton, Sugarcane, Tobacco, Chillies
  - Oilseeds: Groundnut, Sunflower, Castor
  - Pulses: Bengal Gram (Chickpea), Red Gram (Pigeonpea), Green Gram, Black Gram
- **Schema Fields**:
  - `state_name` (VARCHAR): Standardized to "Andhra Pradesh".
  - `district_name` (VARCHAR): District name conforming to Census of India standards.
  - `crop_year` (INTEGER): Agricultural year (e.g., 2018 for 2018-19).
  - `season` (VARCHAR): "Kharif", "Rabi", "Summer", "Whole Year".
  - `crop` (VARCHAR): Standardized common botanical/trade crop name.
  - `area_hectares` (DECIMAL): Total cultivated land in hectares.
  - `production_tonnes` (DECIMAL): Metric tonnes produced.
  - `yield_quintal_per_ha` (DECIMAL): Computed as `(production_tonnes * 10) / area_hectares`.
- **Extraction Strategy**:
  - Ingestion Connector: `ingestion/crop_ingestion.py`.
  - Incremental Strategy: Polling by `crop_year` and `season`.
  - Fallback: Seeded offline baseline dataset covering 2000–2023 for reliable local development without external network dependency.

#### 2.2 Mandi Price & Arrival Ingestion Specification
- **Publisher**: Agricultural Marketing Information Network (AGMARKNET), Govt of India.
- **Major AP Mandis / Markets**:
  - Guntur (World's largest chilli market), Kurnool (Groundnut, Bengal Gram), Vijayawada (Paddy, Maize), Adoni (Cotton), Tirupati (Groundnut), Rajahmundry (Paddy, Oil palm), Anakapalle (Jaggery, Sugarcane).
- **Schema Fields**:
  - `state` (VARCHAR): "Andhra Pradesh"
  - `district` (VARCHAR): District hosting the APMC yard.
  - `market` (VARCHAR): APMC Market yard name.
  - `commodity` (VARCHAR): Agricultural commodity.
  - `variety` (VARCHAR): Specific sub-type / hybrid strain.
  - `arrival_date` (DATE): Format `YYYY-MM-DD`.
  - `min_price_inr` (DECIMAL): Minimum transaction price per quintal (100 kg).
  - `max_price_inr` (DECIMAL): Maximum transaction price per quintal.
  - `modal_price_inr` (DECIMAL): Most frequent transaction price per quintal.
- **Extraction Strategy**:
  - Ingestion Connector: `ingestion/mandi_ingestion.py`.
  - High-Watermark Key: `MAX(arrival_date)`. Only queries records strictly newer than current watermark.
  - Quality Rule: Enforces `min_price <= modal_price <= max_price`. Offending records tagged and redirected to `quarantine_mandi_prices`.

#### 2.3 Meteorological Observations & Forecast Specification
- **Publisher**: IMD / Open-Meteo Historical Weather and Forecast APIs.
- **Grid Coordinates**: Representative centroid coordinates for AP district headquarters (e.g., Guntur: 16.3067° N, 80.4365° E; Kurnool: 15.8281° N, 78.0373° E).
- **Schema Fields**:
  - `location_id` / `district` (VARCHAR)
  - `observation_date` (DATE)
  - `temp_max_c` (DECIMAL): Maximum daily ambient temperature in °C.
  - `temp_min_c` (DECIMAL): Minimum daily ambient temperature in °C.
  - `temp_mean_c` (DECIMAL): Average temperature in °C.
  - `rainfall_mm` (DECIMAL): 24-hour cumulative rainfall in millimeters.
  - `relative_humidity_pct` (DECIMAL): Average relative humidity percentage.
  - `wind_speed_kmh` (DECIMAL): Mean wind speed in km/h.
  - `is_forecast` (BOOLEAN): `FALSE` for observed historical measurements, `TRUE` for forward-looking numerical weather predictions.
- **Extraction Strategy**:
  - Ingestion Connector: `ingestion/weather_ingestion.py`.
  - Retries: 3 attempts with exponential backoff on HTTP 429 (Rate Limit) or 503 (Service Unavailable).

#### 2.4 Soil Health & Nutrient Index Specification
- **Publisher**: Ministry of Agriculture & Farmers Welfare – Soil Health Card Portal.
- **Agro-Ecological Zones Represented**:
  - Coastal Alluvial Soils (Godavari and Krishna deltas)
  - Red Sandy Loams (Chittoor, Anantapur, Nellore)
  - Black Cotton Soils / Vertisols (Guntur, Kurnool, Prakasam)
- **Schema Fields**:
  - `district` (VARCHAR)
  - `soil_type` (VARCHAR): Red, Black Cotton, Alluvial, Coastal Sand, Laterite.
  - `available_nitrogen_kg_ha` (DECIMAL): Low (< 280), Medium (280–560), High (> 560).
  - `available_phosphorus_kg_ha` (DECIMAL): Low (< 10), Medium (10–25), High (> 25).
  - `available_potassium_kg_ha` (DECIMAL): Low (< 108), Medium (108–280), High (> 280).
  - `soil_ph` (DECIMAL): Acidic (< 6.5), Neutral (6.5–7.5), Alkaline (> 7.5).
  - `organic_carbon_pct` (DECIMAL): Percentage organic carbon content.
  - `electrical_conductivity_dsm` (DECIMAL): Soil salinity measure in dS/m.
- **Extraction Strategy**:
  - Ingestion Connector: `ingestion/soil_ingestion.py`.
  - Static survey ingestion with normalization into standardized nutrient status tiers.

#### 2.5 Plant Disease Foliage Image Specification
- **Dataset Reference**: New Plant Diseases Dataset (Vipul Patel / Kaggle).
- **Taxonomy of Covered Crops & Pathologies**:
  - Tomato: Bacterial Spot, Early Blight, Late Blight, Leaf Mold, Septoria Leaf Spot, Spider Mites, Target Spot, Yellow Leaf Curl Virus, Mosaic Virus, Healthy.
  - Potato: Early Blight, Late Blight, Healthy.
  - Pepper Bell: Bacterial Spot, Healthy.
  - Corn (Maize): Cercospora Leaf Spot, Common Rust, Northern Leaf Blight, Healthy.
- **Directory Layout**:
  - `data/raw/plant_disease/train/<class_name>/`
  - `data/raw/plant_disease/valid/<class_name>/`
- **Integrity Verification**: Image headers checked via PIL/OpenCV; truncated or non-JPEG/PNG files rejected at validation phase.

#### 2.6 Agronomy Research & PDF Literature Specification
- **Primary Literature Benchmark**:
  - **Title**: *Plant disease detection and classification techniques: a comparative study of the performances*
  - **Author**: Wubetu Barud Demilie
  - **Journal**: Journal of Big Data (SpringerOpen, 2024), 11:71.
  - **DOI**: `10.1186/s40537-024-00927-1`
  - **Key Themes**: Comparative review of CNNs (AlexNet, VGG, ResNet, MobileNetV2, Inception, EfficientNet), image preprocessing, data augmentation, transfer learning challenges, and edge deployment feasibility.
- **Additional Corpus**: ICAR guidelines on fertilizer scheduling, AP Rythu Bharosa extension circulars, and ANGRAU package of practices.
- **Extraction Rules**:
  - Preserves exact page numbers in chunk metadata.
  - Discards header/footer boilerplate and running headers.
  - Flags scanned or non-searchable PDFs for OCR processing.
