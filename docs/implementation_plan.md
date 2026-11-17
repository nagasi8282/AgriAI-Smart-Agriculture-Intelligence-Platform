# AgriAI: Smart Agriculture Intelligence Platform
## Comprehensive Implementation Plan & Engineering Roadmap

### 1. Executive Summary & Vision
**AgriAI** is an enterprise-grade, end-to-end Smart Agriculture Intelligence Platform tailored primarily for Andhra Pradesh (AP), India, with an extensible architecture for pan-India agricultural intelligence. The platform bridges the gap between raw agronomic data and actionable intelligence by combining:
- **Data Engineering**: Robust Medallion architecture (Bronze -> Silver -> Gold), Snowflake cloud warehousing, dbt transformations, and Apache Airflow orchestration.
- **Predictive Machine Learning**: Crop yield estimation and Mandi modal price forecasting using gradient boosted decision trees and regression techniques with SHAP explainability.
- **Deep Learning & Computer Vision**: MobileNetV2 and EfficientNetB0 transfer learning models for plant leaf disease diagnosis with Grad-CAM visual interpretability, informed by state-of-the-art research (Demilie, 2024).
- **Generative AI & PDF RAG (AgriDoc AI)**: Grounded question-answering over uploaded agricultural research papers, government reports, and extension manuals with strict page-level citation and anti-hallucination guardrails.
- **Unified Modern Interface**: A high-performance Streamlit dashboard backed by a modular FastAPI REST backend and PostgreSQL/S3-compatible data lake.

---

### 2. Phased Development Roadmap

#### Phase 1: Project Foundation & Architectural Setup (Current Phase)
- **Objective**: Establish the repository layout, configuration management, local database connection, FastAPI microservice, Streamlit frontend skeleton, and local Docker Compose infrastructure.
- **Deliverables**:
  1. Complete project directory tree (`app`, `backend`, `ingestion`, `storage`, `data`, `snowflake`, `dbt_agri`, `airflow`, `ml`, `disease_detection`, `ai`, `tests`, `docs`, `scripts`).
  2. Core documentation: `project_charter.md`, `architecture.md`, `dataset_sources.md`, `implementation_plan.md`, `progress.md`.
  3. Environment templates: `.env.example`, `.gitignore`, `requirements.txt`.
  4. Backend skeleton: FastAPI app with health checks, system metadata, CORS, and modular router stubs.
  5. Frontend skeleton: Streamlit multi-page layout with thematic agriculture styling (forest green, emerald, neutral tones).
  6. Docker Compose environment: PostgreSQL, Local Storage, FastAPI, Streamlit.
  7. Phase 1 unit and integration test suite (`tests/unit/test_foundation.py`).

#### Phase 2: Data Collection & Dataset Integration
- **Objective**: Ingest official agricultural datasets for Andhra Pradesh (districts: Guntur, Krishna, Kurnool, Anantapur, East Godavari, Chittoor, Prakasam, etc.) and establish sample data pipelines.
- **Data Sources**:
  - Directorate of Economics & Statistics (DES) / data.gov.in: Crop production, area, and yield (Paddy, Cotton, Groundnut, Maize, Bengal Gram, Chillies, Sugarcane) from 2000–2023.
  - AGMARKNET / Open Government Data: Mandi commodity prices (arrival dates, modal, min, max prices).
  - IMD (India Meteorological Department) / Open-Meteo API: Historical and forecast weather (rainfall, max/min temperature, relative humidity).
  - Soil Health Card Portal: N-P-K, pH, Organic Carbon, and EC distributions across AP agro-climatic zones.
  - PlantVillage / New Plant Diseases Dataset: Tomato, Potato, Corn, Pepper leaf images.
  - Agricultural PDF Corpus: Research papers (including Demilie 2024), ICAR advisories, and AP Rythu Bharosa manuals.
- **Deliverables**: Ingestion connectors in `ingestion/` with schema validation, watermark tracking, raw local storage dumps, and sample seed data in `data/sample/`.

#### Phase 3: Data Engineering & Medallion Architecture
- **Objective**: Implement the data pipeline moving raw ingested records into Bronze, Silver, and Gold layers.
- **Deliverables**:
  - **Bronze**: Append-only raw data ingestion with source metadata, ingest timestamps, and partition keys.
  - **Silver**: Deduplication, type casting, district/crop name standardization (handling phonetic spelling variations), range validations, quarantine table for malformed records.
  - **Gold**: Dimensional star schema (`DIM_DATE`, `DIM_LOCATION`, `DIM_CROP`, `DIM_MARKET`, `FACT_CROP_PRODUCTION`, `FACT_WEATHER`, `FACT_MANDI_PRICE`, `FACT_SOIL`, `FACT_YIELD_PREDICTION`, `FACT_DISEASE_PREDICTION`).
  - Great Expectations / custom SQL data quality assertions.

#### Phase 4: Snowflake Cloud Warehousing & dbt Transformations
- **Objective**: Cloud analytics warehouse configuration and dbt models.
- **Deliverables**:
  - Snowflake setup scripts (`snowflake/01_setup.sql` through `04_warehouse_models.sql`): roles, virtual warehouses, databases (`AGRIAI_RAW`, `AGRIAI_ANALYTICS`), stages, external S3 stages.
  - `dbt_agri` project: `staging` views/tables, `marts` facts and dimensions, tests (`not_null`, `unique`, accepted values, referential integrity).

#### Phase 5: Apache Airflow Orchestration
- **Objective**: Production-grade orchestration for scheduled ingestion and transformation.
- **Deliverables**:
  - Airflow Docker Compose with Celery/Local Executor.
  - Main DAG: `agri_daily_etl_dag.py` running ingestion -> bronze load -> dbt staging -> dbt marts -> data quality checks.
  - Airflow connection configurations, retry policies with exponential backoff, SLA tracking, and alert triggers.

#### Phase 6: Machine Learning Pipelines
- **Objective**: Develop, validate, and serve predictive models for crop yield, mandi price, and soil-based fertilizer support.
- **Models**:
  1. **Crop Yield Prediction**: Random Forest Regressor & XGBoost Regressor trained on weather, soil, area, and historical yield data. Chronological train/test split. Evaluation via MAE, RMSE, R². SHAP feature attribution.
  2. **Mandi Price Prediction**: Time-series aware regression model for commodity modal prices across key AP markets. Evaluation via MAE, RMSE, MAPE.
  3. **Fertilizer Support System**: Transparent agronomic rule engine combined with multiclass classifier for NPK optimization based on ICAR fertilizer schedules for AP soils.
- **Deliverables**: Model training scripts, serialized artifacts (`.joblib`/`.onnx`), evaluation benchmarks, and FastAPI inference endpoints.

#### Phase 7: Deep Learning Plant Disease Detection
- **Objective**: Implement computer vision classification for crop foliage diseases with Grad-CAM heatmaps.
- **Scientific Foundation**: Guided by Demilie (2024) "Plant disease detection and classification techniques: a comparative study of the performances", Journal of Big Data.
- **Architectures**:
  - Candidate 1: MobileNetV2 (efficient, edge/mobile friendly, depthwise separable convolutions).
  - Candidate 2: EfficientNetB0 (compound scaling for high accuracy-to-compute ratio).
- **Deliverables**:
  - Dataset pipeline with augmentation (training set only: flips, rotations, color jitter), resizing (224x224), and normalization.
  - Training, validation, and testing scripts with strict separation preventing data leakage.
  - Grad-CAM visual explanation overlay generation.
  - Out-of-distribution (OOD) confidence thresholding to reject non-leaf or unsupported images.
  - Comprehensive Model Card (`disease_detection/README.md`) and comparative evaluation table.

#### Phase 8: Generative AI & AgriDoc AI (PDF RAG)
- **Objective**: Provide conversational assistance and grounded PDF question answering.
- **Components**:
  - **AgriAI Assistant**: Conversational agent configured with agricultural domain guardrails, data retrieval tool for real-time market/weather/crop data, preventing hallucinations.
  - **AgriDoc AI (PDF RAG)**:
    - Multi-PDF document upload and processing via PyMuPDF.
    - Page-aware semantic text chunking with overlap.
    - Dense vector embeddings via `sentence-transformers/all-MiniLM-L6-v2`.
    - Local vector storage with FAISS / ChromaDB.
    - Strict citation generator providing Document Name, Page Number, and extracted verbatim snippet.
- **Deliverables**: AI service layer, vector indexing pipeline, chat interface with source citations.

#### Phase 9: Unified Streamlit Application
- **Objective**: Assemble a multi-page, responsive, agriculture-themed web platform.
- **Pages**:
  1. *Home Dashboard*: High-level metrics, active districts, weather snippet, production summary, freshness indicator.
  2. *Crop Intelligence*: Deep dive into AP crop trends, area vs production, yield trends.
  3. *Weather Intelligence*: Rainfall patterns, temperature anomalies, district-level climate metrics.
  4. *Mandi Price Intelligence*: Commodity price movements, modal price trends, market comparison.
  5. *Soil & Fertilizer Support*: NPK input form, nutrient deficiency diagnosis, official advisory notices.
  6. *Crop Yield Prediction*: Interactive inference form, yield prediction in quintals/hectare, SHAP explanation.
  7. *Mandi Price Prediction*: Horizon-based commodity price forecasting with historical trend overlay.
  8. *Plant Disease Detection*: Drag-and-drop leaf image upload, prediction with top-3 confidence bars, Grad-CAM heatmap visualization, and disclaimers.
  9. *AgriAI Assistant*: Natural language chat with agricultural context memory.
  10. *AgriDoc AI*: Research document upload, chunk indexer, RAG chat with side-by-side page citations.
  11. *Reports & Export*: One-click CSV and PDF summary generator for farmer/extension officer use.
  12. *About & Academic Documentation*: M.Tech dissertation summary, literature references, system architecture.

#### Phase 10: Testing, CI/CD, Containerization & Academic Thesis Deliverables
- **Objective**: Comprehensive validation, packaging, and dissertation-grade academic documentation.
- **Deliverables**:
  - Full test suite: Unit tests, integration tests, API contract tests, ML inference tests.
  - Production Docker Compose configuration.
  - Complete Academic Documentation in `docs/` (Abstract, Methodology, Experimental Results, Literature Review, Comparative Studies).
  - Operational Runbook for deployment and disaster recovery.

---

### 3. Immediate Phase 1 Execution Checklist
- [x] Create implementation plan (`docs/implementation_plan.md`)
- [ ] Create repository directory tree
- [ ] Write `docs/project_charter.md`
- [ ] Write `docs/architecture.md` (with Mermaid diagrams)
- [ ] Write `docs/dataset_sources.md`
- [ ] Write `.env.example` and `.gitignore`
- [ ] Write `requirements.txt` and verify dependencies
- [ ] Implement backend core: `backend/main.py`, config, schemas, routers
- [ ] Implement frontend core: `app/Home.py`, navigation, theme, style
- [ ] Create local storage abstractions and sample data directory
- [ ] Create Docker Compose for Phase 1 local development
- [ ] Create `README.md` and `docs/progress.md`
- [ ] Implement unit and integration tests for Phase 1
- [ ] Execute tests, verify backend & frontend startup, report results to user
