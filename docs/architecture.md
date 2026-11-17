# AgriAI: Smart Agriculture Intelligence Platform
## Complete System Architecture & Technical Design

### 1. Architectural Blueprint
AgriAI is designed as an end-to-end modern data and AI platform, following a decoupled microservices architecture with a Medallion Data Lakehouse, an AI/ML intelligence layer, a Generative AI RAG engine, and a presentation dashboard.

```mermaid
flowchart TD
    subgraph SOURCELAYER["1. Multi-Modal Agriculture Data Sources"]
        S1["Crop Production Statistics<br/>(DES / data.gov.in)"]
        S2["Mandi Prices & Arrivals<br/>(AGMARKNET)"]
        S3["Meteorological Data<br/>(IMD / Open-Meteo)"]
        S4["Soil Health Cards<br/>(MoA&FW / AP Soil Portal)"]
        S5["Plant Disease Imagery<br/>(PlantVillage / Kaggle)"]
        S6["Agronomy Literature & PDFs<br/>(ICAR, Demilie 2024, Manuals)"]
    end

    subgraph INGESTION["2. Ingestion & Orchestration Layer"]
        ING1["Crop Ingest Connector<br/>(CSV / Rest API)"]
        ING2["Mandi Ingest Connector<br/>(Incremental / Date Watermark)"]
        ING3["Weather Ingest Connector<br/>(Scheduled API Poller)"]
        ING4["Soil Ingest Connector<br/>(Schema Validator)"]
        ING5["Image & PDF Ingest<br/>(FastAPI Multi-part Upload)"]
        AIRFLOW["Apache Airflow 2.x<br/>(DAG Orchestration & Retries)"]
    end

    subgraph STORAGE["3. Medallion Storage & Warehouse Layer"]
        subgraph BRONZE["Bronze Zone (Raw & Immutable)"]
            B_LOCAL["Local Filesystem Lake / S3 Raw<br/>(Partitioned by Domain/Year/Month)"]
            B_SNOW["Snowflake RAW DB / Postgres Raw"]
        end
        subgraph SILVER["Silver Zone (Cleaned & Conformed)"]
            S_DBT["dbt Transformations & Data Quality<br/>(Deduplication, Standardized AP Districts/Crops)"]
            S_SNOW["Snowflake STAGING / Postgres Clean"]
        end
        subgraph GOLD["Gold Zone (Analytical Data Marts)"]
            G_DIM["Dimensions:<br/>DIM_DATE, DIM_LOCATION, DIM_CROP, DIM_MARKET"]
            G_FACT["Facts:<br/>FACT_CROP_PRODUCTION, FACT_MANDI_PRICE,<br/>FACT_WEATHER, FACT_SOIL"]
        end
    end

    subgraph AIML["4. Intelligence & Serving Layer"]
        ML_YIELD["Crop Yield Model<br/>(RandomForest / XGBoost + SHAP)"]
        ML_PRICE["Mandi Price Model<br/>(Time-Series Regression)"]
        DL_VISION["Plant Pathology Classifier<br/>(MobileNetV2 / EfficientNetB0 + Grad-CAM)"]
        RAG_ENGINE["AgriDoc AI RAG Pipeline<br/>(PyMuPDF + MiniLM Embeddings + FAISS / ChromaDB)"]
        API["FastAPI Backend Services<br/>(REST API, Pydantic, CORS, Logging)"]
    end

    subgraph FRONTEND["5. User Presentation Layer"]
        ST_HOME["Home & KPI Dashboard"]
        ST_CROP["Crop & Weather Intelligence"]
        ST_MANDI["Mandi Price Analytics"]
        ST_PRED["Yield & Price Prediction"]
        ST_VISION["Plant Disease Diagnosis"]
        ST_RAG["AgriDoc AI Research Assistant"]
        ST_REP["Reports & Exports (CSV/PDF)"]
    end

    SOURCELAYER --> INGESTION
    AIRFLOW -.-> INGESTION
    INGESTION --> BRONZE
    BRONZE --> SILVER
    SILVER --> GOLD
    GOLD --> API
    AIML <--> API
    API --> FRONTEND
```

---

### 2. End-to-End Data Flow

```mermaid
sequenceDiagram
    autonumber
    actor Farmer as User / Researcher / Extension Officer
    participant UI as Streamlit Frontend (Port 8501)
    participant API as FastAPI Gateway (Port 8000)
    participant RAG as AgriDoc AI / Vector Store
    participant Vision as Deep Learning / Grad-CAM
    participant ML as ML Inference Engine
    participant DB as Gold Marts (PostgreSQL / Snowflake)
    participant Lake as Bronze Data Lake (Local / AWS S3)

    %% Scenario A: Analytical Query
    Farmer->>UI: Selects AP District (Guntur) & Crop (Paddy)
    UI->>API: GET /api/v1/analytics/production?district=Guntur&crop=Paddy
    API->>DB: Query FACT_CROP_PRODUCTION & DIM_LOCATION
    DB-->>API: Filtered historical time-series records
    API-->>UI: Structured JSON response
    UI-->>Farmer: Renders interactive Plotly trend & area vs yield graphs

    %% Scenario B: Foliage Disease Detection
    Farmer->>UI: Uploads tomato leaf image with lesions
    UI->>API: POST /api/v1/disease/predict (multipart/form-data)
    API->>Vision: Preprocess (224x224), infer via MobileNetV2 / EfficientNetB0
    Vision->>Vision: Compute Grad-CAM heatmaps on target convolutional layer
    Vision-->>API: Predicted Class, Confidence (96.4%), Top-3 Alternatives, Heatmap Base64
    API-->>UI: Diagnosis JSON + Visual Explanation
    UI-->>Farmer: Displays disease details, confidence, Grad-CAM overlay & advisory disclaimer

    %% Scenario C: AgriDoc AI PDF Query
    Farmer->>UI: Uploads ICAR / Demilie 2024 PDF & asks question
    UI->>API: POST /api/v1/documents/ask {query, doc_id}
    API->>RAG: Generate query embedding, search FAISS top-k chunks
    RAG->>RAG: Ground LLM prompt with retrieved passages & metadata
    RAG-->>API: Synthesized answer + exact Page Citations & snippets
    API-->>UI: Grounded answer with expandable source passages
    UI-->>Farmer: Displays answer with verbatim citations
```

---

### 3. Medallion Data Warehouse Architecture

The data architecture organizes information into three distinct zones ensuring data lineage, governance, and auditability:

#### 3.1 Bronze Layer (Raw & Immutable)
- **Purpose**: Capture source data exactly as provided by upstream producers without alteration.
- **Format**: Parquet or raw CSV files partitioned chronologically (`/data/raw/{domain}/year={YYYY}/month={MM}/`).
- **Audit Columns**: Every bronze record carries:
  - `_ingest_id`: UUID generated at extraction time.
  - `_source_system`: Name of source (e.g., `agmarknet_portal`, `data_gov_in_ap`).
  - `_ingested_at`: UTC timestamp of extraction.
  - `_file_checksum`: SHA-256 hash of the ingested payload.

#### 3.2 Silver Layer (Cleaned, Standardized & Conformed)
- **Purpose**: Clean, standardize, and validate data across disparate providers.
- **Transformations Handled**:
  - District name canonicalization (e.g., standardizing "Y.S.R. Kadapa", "Kadapa", "Cuddapah" to `YSR Kadapa`).
  - Crop nomenclature unification (e.g., mapping "Paddy", "Rice", "Dhan" to `Paddy (Dhan)`).
  - Type conversions: dates to ISO-8601 `YYYY-MM-DD`, currency to `DECIMAL(10, 2)`, quantities to metric units (`hectares`, `metric tonnes`, `quintals`).
  - Data quarantine: Records violating domain sanity checks (e.g., `min_price > max_price` or `production < 0`) are written to an isolated quarantine table with error taxonomy tags.

#### 3.3 Gold Layer (Dimensional Star Schema)
- **Purpose**: Business-ready, high-performance analytical marts optimized for analytical slicing, reporting, and ML feature stores.

```mermaid
erDiagram
    DIM_DATE ||--o{ FACT_CROP_PRODUCTION : "date_id"
    DIM_LOCATION ||--o{ FACT_CROP_PRODUCTION : "location_id"
    DIM_CROP ||--o{ FACT_CROP_PRODUCTION : "crop_id"

    DIM_DATE ||--o{ FACT_MANDI_PRICE : "date_id"
    DIM_LOCATION ||--o{ FACT_MANDI_PRICE : "location_id"
    DIM_CROP ||--o{ FACT_MANDI_PRICE : "crop_id"
    DIM_MARKET ||--o{ FACT_MANDI_PRICE : "market_id"

    DIM_DATE ||--o{ FACT_WEATHER : "date_id"
    DIM_LOCATION ||--o{ FACT_WEATHER : "location_id"

    DIM_LOCATION ||--o{ FACT_SOIL : "location_id"

    DIM_DATE {
        int date_id PK
        date calendar_date
        int year
        int month
        varchar season
        int quarter
    }

    DIM_LOCATION {
        int location_id PK
        varchar state
        varchar district
        varchar agro_climatic_zone
        decimal latitude
        decimal longitude
    }

    DIM_CROP {
        int crop_id PK
        varchar crop_name
        varchar crop_category
        varchar botanical_name
        varchar major_growing_season
    }

    DIM_MARKET {
        int market_id PK
        varchar market_name
        varchar district
        varchar apmc_code
    }

    FACT_CROP_PRODUCTION {
        bigint production_id PK
        int date_id FK
        int location_id FK
        int crop_id FK
        decimal area_hectares
        decimal production_tonnes
        decimal yield_quintal_per_ha
    }

    FACT_MANDI_PRICE {
        bigint mandi_price_id PK
        int date_id FK
        int location_id FK
        int crop_id FK
        int market_id FK
        decimal arrival_tonnes
        decimal min_price_inr
        decimal max_price_inr
        decimal modal_price_inr
    }

    FACT_WEATHER {
        bigint weather_id PK
        int date_id FK
        int location_id FK
        decimal rainfall_mm
        decimal temp_max_c
        decimal temp_min_c
        decimal relative_humidity_pct
        decimal wind_speed_kmh
    }

    FACT_SOIL {
        bigint soil_id PK
        int location_id FK
        decimal nitrogen_kg_ha
        decimal phosphorus_kg_ha
        decimal potassium_kg_ha
        decimal soil_ph
        decimal organic_carbon_pct
        decimal electrical_conductivity_dsm
        varchar soil_type
    }
```

---

### 4. Dual-Deployment Strategy (Local vs Cloud)

| Capability | Local Development Environment | Cloud Production Environment |
| :--- | :--- | :--- |
| **Relational / Warehouse DB** | PostgreSQL 16 (Local / Docker) | Snowflake (Cloud Analytics Warehouse) |
| **Object Lake Storage** | Local directory (`data/raw/`) or MinIO S3 API | AWS S3 Bucket (`s3://agriai-data-lake-prod/`) |
| **Transformations** | dbt Core (`dbt-postgres`) / Python scripts | dbt Core (`dbt-snowflake`) |
| **Pipeline Orchestrator** | Apache Airflow in Docker Compose | Managed Airflow (AWS MWAA or Cloud Docker) |
| **Vector DB** | FAISS CPU / ChromaDB local file store | ChromaDB Server / Milvus / Pinecone |
| **Application Layer** | FastAPI + Streamlit on localhost | AWS ECS / EKS / Cloud Run or EC2 |

The codebase uses abstract factory interfaces for Storage and Database drivers. When cloud environment credentials (`SNOWFLAKE_ACCOUNT`, `AWS_ACCESS_KEY_ID`) are absent, the application gracefully initializes its PostgreSQL/Local-File driver without throwing runtime exceptions.

---

### 5. AI/ML and Generative AI Architectural Pipeline

#### 5.1 Machine Learning Pipelines
- **Crop Yield Predictor**:
  - Inputs: `crop_name`, `district`, `season`, `area_hectares`, `rainfall_mm`, `temp_avg_c`, `nitrogen`, `phosphorus`, `potassium`, `soil_ph`.
  - Feature Engineering: One-hot/target encoding for categorical inputs, standard scaling for numeric features, temporal feature indicators.
  - Algorithms: Random Forest Regressor and XGBoost Regressor with cross-validated hyperparameter optimization.
  - Explainability: TreeSHAP computes global summary plots and local force plots explaining positive and negative feature contributions.
- **Mandi Price Forecaster**:
  - Time-series windowing with rolling 7-day, 14-day, and 30-day price lags and arrival volume indicators to forecast future modal prices.

#### 5.2 Deep Learning Foliage Pathology Pipeline
- **Backbone Architectures**:
  - **MobileNetV2**: 3.5M parameters, depthwise separable convolutions, ideal for resource-constrained field deployment.
  - **EfficientNetB0**: 5.3M parameters, compound coefficient scaling balancing depth, width, and resolution.
- **Literature Alignment**: Implements the comparative methodology outlined by Demilie (2024), comparing macro-accuracy, precision, recall, F1, inference latency, and memory footprints.
- **Visual Saliency**: Grad-CAM captures gradients flowing into the final convolutional layer (e.g., `features.18` in MobileNetV2 or `conv_head` in EfficientNetB0) to generate a high-contrast heatmap over diseased leaf regions.

#### 5.3 AgriDoc AI (Grounded RAG Pipeline)
- **Ingestion**: PyMuPDF extracts text page-by-page, attaching metadata `{document_name, page_number, total_pages}`.
- **Chunking**: RecursiveCharacterTextSplitter with chunk size 600 characters and 100 character overlap.
- **Embeddings**: SentenceTransformers `all-MiniLM-L6-v2` generating 384-dimensional dense vectors.
- **Vector Search**: FAISS IndexFlatIP (Cosine similarity) or ChromaDB returning top-k passages with similarity score thresholds.
- **Synthesis & Anti-Hallucination**: Prompt template instructing the LLM to reply strictly from supplied context and format bracketed citations `[Document: <name>, Page: <page_no>]`.
