# AgriAI: Smart Agriculture Intelligence Platform
## Project Charter & Formal Requirements Specification

### 1. Document Control
- **Project Name:** AgriAI – Smart Agriculture Intelligence Platform
- **Document Version:** 1.0.0
- **Status:** Baseline Approved
- **Lead Role:** Senior Data & AI Engineer / Solutions Architect
- **Academic Degree:** Master of Technology (M.Tech) in Computer Science & Engineering / Data Engineering
- **Target Geographical Region:** Andhra Pradesh (AP), India (Scalable to Pan-India)

---

### 2. Executive Summary & Business Objective
Agriculture is the foundational pillar of the Andhra Pradesh economy, supporting over 60% of its rural population across coastal deltas, dryland Rayalaseema, and fertile plateau agro-ecological zones. However, farmers, agronomists, extension officers, and policy researchers face critical challenges:
1. **Siloed and Fragmented Data**: Crop production data, mandi market prices, soil fertility indices, and weather trends reside across disconnected government portals (data.gov.in, AGMARKNET, IMD, Soil Health Card).
2. **Delayed Market & Agronomic Intelligence**: Farmers frequently sell produce at distressed rates due to lack of transparent local mandi price forecasts and historical commodity trend analytics.
3. **Crop Yield Uncertainty**: Extreme climatic variability (cyclones in Coastal AP, droughts in Rayalaseema) makes yield estimation difficult without integrated meteorological and agronomic machine learning models.
4. **Plant Pathology Diagnosis Bottlenecks**: Pathogen attacks and foliar diseases cause severe yield reductions (15%–40%). Rural farmers lack immediate access to plant pathologists for leaf diagnosis.
5. **Information Access Inequity**: Extensive research publications, ICAR advisories, and AP Rythu Bharosa manuals are locked in multi-page PDF documents inaccessible to conversational querying.

**AgriAI's Core Objective**: Build an integrated, open, end-to-end data engineering and artificial intelligence platform combining modern medallion data warehousing (Bronze, Silver, Gold), cloud integration (AWS S3 & Snowflake), predictive machine learning (yield and mandi price forecasting), deep learning computer vision (leaf disease detection with Grad-CAM), and retrieval-augmented generative AI (AgriDoc AI) to empower agricultural stakeholders.

---

### 3. Problem Statement & Research Scope
#### 3.1 Problem Statement
"How can distributed multi-modal agricultural datasets—spanning structured time-series (production, mandi arrivals, meteorological observations, soil profiles), unstructured foliar images, and agricultural literature—be ingested, harmonized into a governed medallion warehouse, and leveraged through predictive ML, transfer learning vision models, and grounded generative AI to deliver actionable, verifiable agronomic insights for Andhra Pradesh?"

#### 3.2 In-Scope
- Ingestion connectors for Andhra Pradesh crop statistics (13 legacy / 26 reorganized districts: Guntur, Krishna, Kurnool, Anantapur, East Godavari, Chittoor, Prakasam, etc.).
- Major crops of Andhra Pradesh: Paddy (Rice), Cotton, Groundnut, Maize, Bengal Gram (Chickpea), Chillies, Sugarcane, Pulses.
- Time-series market data: AGMARKNET daily arrivals, minimum, maximum, and modal prices (INR/Quintal).
- Weather observations: Historical and forecast rainfall (mm), max/min temperature (°C), relative humidity (%).
- Soil health indicators: Nitrogen (N), Phosphorus (P), Potassium (K), Soil pH, Organic Carbon (OC), Electrical Conductivity (EC).
- Deep learning computer vision: Multi-class foliage disease classification using MobileNetV2 and EfficientNetB0 with Grad-CAM saliency heatmaps.
- AgriDoc AI: RAG pipeline over agricultural research papers (specifically incorporating Demilie 2024 literature) and extension bulletins with page-level citations.
- Dual-deployment readiness: 100% self-contained local developer mode (PostgreSQL + Local Data Lake) and Cloud Enterprise mode (AWS S3 + Snowflake + Airflow).

#### 3.3 Out-of-Scope
- Prescriptive chemical or pesticide dosage calculations (legal and biological safety restrictions).
- Unverified automated trading or direct transactional execution on mandi APMC portals.
- Fabrication of live sensor readings when field IoT hardware is absent.

---

### 4. Stakeholder & User Personas

| Persona | Primary Needs & Use Cases | Platform Touchpoint |
| :--- | :--- | :--- |
| **Progressive Farmer / FPO Manager** | Mandi price trends, fair market value forecasts, weather alerts, rapid crop leaf disease diagnosis from smartphone images. | Streamlit Mobile/Desktop UI, Mandi Intelligence, Disease Detection. |
| **Agricultural Extension Officer (Rythu Bharosa Kendras)** | Soil test interpretation, NPK fertilizer guideline lookups, crop advisory literature search. | Soil Recommendation Support, AgriDoc AI RAG. |
| **Agronomy Researcher / Academician** | Historical multi-decade production analysis, correlation between rainfall anomalies and yield across Rayalaseema vs Coastal AP. | Crop Intelligence, Export Reports, Data Warehouse. |
| **Data Engineer / ML Engineer** | Airflow DAG health, pipeline latency, dbt transformation logs, data drift, model evaluation metrics. | FastAPI Swagger docs, Airflow UI, MLflow/Metrics logs. |

---

### 5. Functional Requirements (FR)

#### FR-1: Data Ingestion & Storage
- **FR-1.1**: The platform shall ingest structured CSV/JSON datasets with full and incremental extraction mechanisms.
- **FR-1.2**: Ingestion routines shall compute and track ingestion watermarks, row counts, and cryptographic checksums.
- **FR-1.3**: Raw data must be written immutably to the Bronze zone with partition scheme: `data/raw/{domain}/year={YYYY}/month={MM}/`.
- **FR-1.4**: Ingestion failures must be trapped, logged with stack traces, and quarantined without blocking subsequent pipeline tasks.

#### FR-2: Transformation & Data Quality
- **FR-2.1**: The Silver layer shall standardize district names (handling variations like "East Godavari" vs "E. Godavari") and crop names.
- **FR-2.2**: Business validation rules must verify: `min_price <= modal_price <= max_price`, non-negative acreage and production, valid calendar dates, and realistic weather ranges.
- **FR-2.3**: The Gold layer shall expose star schema analytical marts (`DIM_DATE`, `DIM_LOCATION`, `DIM_CROP`, `DIM_MARKET`, `FACT_CROP_PRODUCTION`, `FACT_WEATHER`, `FACT_MANDI_PRICE`, `FACT_SOIL`).

#### FR-3: Predictive Machine Learning
- **FR-3.1 (Crop Yield)**: Train regressors (Random Forest, XGBoost) to predict yield (Quintals/Hectare) given crop, district, season, area, weather, and soil features.
- **FR-3.2 (Mandi Price)**: Provide time-series price forecasts for major commodities across AP mandis, reporting MAE, RMSE, and MAPE.
- **FR-3.3 (Explainability)**: The model serving layer shall compute and display SHAP value feature attributions for individual yield predictions.
- **FR-3.4 (Fertilizer Support)**: Transparent rule engine encoding official ICAR/ANGRAU nutrient balance matrices based on soil test inputs.

#### FR-4: Deep Learning Foliage Disease Diagnosis
- **FR-4.1**: Fine-tune MobileNetV2 and EfficientNetB0 on agricultural foliage disease datasets.
- **FR-4.2**: Generate Grad-CAM heatmaps overlaying the original image to visually explain model attention regions.
- **FR-4.3**: Provide confidence scores, top-3 class probabilities, and an Out-of-Distribution (OOD) rejection threshold for non-leaf or uncertain inputs.
- **FR-4.4**: Clearly present expert consultation disclaimers on all diagnostic outputs.

#### FR-5: Generative AI & AgriDoc AI (PDF RAG)
- **FR-5.1**: Enable drag-and-drop upload of agricultural PDF reports, research papers, and advisories.
- **FR-5.2**: Extract text page-by-page preserving structural page metadata using PyMuPDF.
- **FR-5.3**: Chunk documents semantically with recursive character splitters and index dense embeddings into vector storage (FAISS / ChromaDB).
- **FR-5.4**: Ground LLM answers strictly on retrieved document passages, generating unambiguous citations (Document Name, Page Number, Verbatim Snippet).
- **FR-5.5**: Refuse hallucinated responses when evidence is not present in the indexed documents.

#### FR-6: User Interface & Reporting
- **FR-6.1**: Provide a multi-page Streamlit application styled with high-contrast, agriculture-tailored design tokens.
- **FR-6.2**: Render interactive Plotly charts with dynamic filtering by State, District, Crop, Season, and Year.
- **FR-6.3**: Enable downloadable CSV and formatted PDF summary reports with generated timestamps and disclaimer notices.

---

### 6. Non-Functional Requirements (NFR)

- **NFR-1 (Performance & Latency)**: REST API response times for analytical aggregations shall not exceed 1.5 seconds. ML inference shall execute within 200 milliseconds. Image classification with Grad-CAM generation shall complete within 1.2 seconds on CPU.
- **NFR-2 (Reliability & Resilience)**: All pipeline components must have retry policies with exponential backoff (initial delay: 5s, max retries: 3). Failed ingestion batches must not corrupt existing historical data.
- **NFR-3 (Modularity & Decoupling)**: Frontend components must interface with backend services strictly via REST APIs and well-defined Pydantic schemas.
- **NFR-4 (Security & Compliance)**: No API keys, cloud tokens, or database credentials shall be committed to version control. Configuration must be injected via `.env` environment variables.
- **NFR-5 (Reproducibility)**: The entire platform must be buildable via Docker Compose and runnable in standard developer environments without proprietary external lock-in.

---

### 7. SLAs, RPO, and Data Freshness Targets

| Data Domain | Update Cadence | Target Freshness | SLA for Pipeline Completion | Recovery Point Objective (RPO) |
| :--- | :--- | :--- | :--- | :--- |
| **Mandi Market Prices** | Daily (Mon–Sat) | Ingested by 08:00 AM IST | <= 30 minutes | 24 Hours |
| **Weather Observations** | Daily / 6-hourly | <= 6 hours old | <= 15 minutes | 6 Hours |
| **Crop Production** | Seasonal / Annual | Updated on official release | <= 1 hour | N/A (Historical Archive) |
| **Soil Health Indices** | Semi-annual / Annual | Baseline updated bi-annually| <= 1 hour | N/A (Static Survey) |
| **Model Retraining** | Monthly / On-Demand | Versioned artifact release | Batch run overnight | Model checkpoint rollback |

---

### 8. Project Assumptions & Limitations
1. **Academic Demonstration Mode**: High-volume paid external cloud APIs (e.g. proprietary weather feeds or commercial LLMs) are abstracted so the application operates seamlessly with open APIs, local embeddings, and local seed data when external credentials are not supplied.
2. **Field Image Generalization**: The leaf disease model trained on laboratory or controlled-background datasets (e.g., PlantVillage) may experience performance shifts under direct sunlight, complex soil backgrounds, or multiple concurrent diseases. This limitation is explicitly acknowledged and highlighted in the UI and documentation.
3. **Regulatory Compliance**: The platform strictly serves as an informational decision-support aid and does not constitute legally certified agricultural extension advice.
