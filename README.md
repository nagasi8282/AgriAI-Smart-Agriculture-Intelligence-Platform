# AgriAI – Smart Agriculture Intelligence Platform

[![Python 3.12](https://img.shields.io/badge/Python-3.12-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B.svg)](https://streamlit.io/)
[![Architecture](https://img.shields.io/badge/Architecture-Medallion%20Lakehouse-blue.svg)](docs/architecture.md)
[![Target Region](https://img.shields.io/badge/Focus-Andhra%20Pradesh%20(India)-darkgreen.svg)](docs/project_charter.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise-grade, end-to-end Smart Agriculture Intelligence Platform integrating **Medallion Data Engineering (Bronze, Silver, Gold)**, **Cloud Warehousing (Snowflake & AWS S3)**, **Predictive Machine Learning (Yield & Price Forecasting with TreeSHAP)**, **Deep Learning Computer Vision (Plant Disease Diagnosis with Grad-CAM)**, and **Generative AI (AgriDoc AI PDF RAG with Page Citations)** tailored for **Andhra Pradesh, India**.

Inspired by modern end-to-end data engineering architecture (such as [darshilparmar/zomato-ai-data-engineering-end-to-end-project](https://github.com/darshilparmar/zomato-ai-data-engineering-end-to-end-project)), adapted and engineered from the ground up for the agricultural domain.

---

## 🌾 Platform Architecture Overview

```
AGRICULTURE SOURCES (Crop Statistics, Mandi Prices, IMD Weather, Soil Health, Foliage Images, Research PDFs)
         ↓
DATA INGESTION LAYER (Python Connectors, High-Watermark Tracking, Schema Validation, Retries)
         ↓
DATA LAKE (Local Partitioned Storage / AWS S3: Bronze Zone)
         ↓
TRANSFORMATION & DATA WAREHOUSE (dbt Core + PostgreSQL / Snowflake: Silver & Gold Star Schema)
         ↓
ORCHESTRATION (Apache Airflow 2.x Scheduled DAGs)
         ↓
AI & MACHINE LEARNING LAYER (Random Forest + XGBoost + SHAP | MobileNetV2 + Grad-CAM)
         ↓
GENERATIVE AI LAYER (AgriAI Assistant & AgriDoc AI PDF RAG with Page Citations)
         ↓
PRESENTATION DASHBOARD (Multi-Page Streamlit App with Interactive Plotly Visualizations)
```

For the complete technical blueprint and sequence diagrams, see [docs/architecture.md](docs/architecture.md).

---

## 🚀 Key Modules & Capabilities

1. **Dashboard Overview**: KPI cards, district coverage, live freshness badges, and agro-climatic summaries.
2. **Crop Intelligence**: Multi-year time-series exploration of AP crop area, production, and yield.
3. **Weather Intelligence**: District-level rainfall anomalies, temperature trends, and climate indicators.
4. **Mandi Price Intelligence**: AGMARKNET wholesale prices, trading spreads, and APMC yard comparisons.
5. **Soil & Fertilizer Support**: Soil Health Card nutrient classification and transparent ICAR/ANGRAU split fertilizer scheduling.
6. **Crop Yield Prediction**: Machine learning regression estimating quintals/ha with TreeSHAP feature attributions.
7. **Mandi Price Forecasting**: Time-series aware regression model projecting commodity modal prices.
8. **Plant Disease Detection**: Deep learning foliage classifier (MobileNetV2 / EfficientNetB0) generating Grad-CAM visual saliency heatmaps, guided by *Demilie (2024), Journal of Big Data*.
9. **AgriAI Assistant**: Conversational assistant grounded in regional agricultural datasets.
10. **AgriDoc AI (PDF RAG)**: Question-answering over uploaded agricultural literature with exact document and page citations.
11. **Reports & Exports**: One-click CSV and formatted audit summary exports.
12. **Academic & Thesis Profile**: M.Tech thesis documentation, methodology, and model cards.

---

## 🛠️ Quick Start & Local Setup

### Prerequisites
- Python 3.10 – 3.12
- Docker & Docker Compose (optional for containerized run)
- Git

### 1. Clone & Set Up Environment
```bash
# Clone the repository
git clone https://github.com/your-username/AgriAI.git
cd AgriAI

# Create and activate virtual environment
python -m venv .venv

# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Linux / macOS:
source .venv/bin/activate

# Install core dependencies
pip install -r requirements.txt
```

### 2. Configure Environment Variables
```bash
# Copy example configuration template
cp .env.example .env
```
*(All local defaults operate seamlessly without external API keys or cloud credentials).*

### 3. Generate Validated Sample Data
```bash
python scripts/generate_sample_data.py
```
This generates authentic, calibrated baseline records for Andhra Pradesh covering 13 districts:
- 819 Crop Production records (2015–2023)
- 1,560 Mandi Wholesale Price records
- 1,573 Weather Observation records
- 13 District Soil Health profiles

### 4. Run the Backend API (FastAPI)
```bash
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```
- Interactive Swagger UI: [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
- Health Check: [http://localhost:8000/health](http://localhost:8000/health)

### 5. Run the Frontend Dashboard (Streamlit)
In a separate terminal:
```bash
streamlit run app/Home.py --server.port 8501
```
Access the application at: [http://localhost:8501](http://localhost:8501)

### 6. Run via Docker Compose (Alternative)
```bash
docker-compose up --build -d
```
Starts PostgreSQL (5432), FastAPI (8000), and Streamlit (8501) concurrently.

---

## 🧪 Running Automated Tests

AgriAI includes an extensive test suite verifying API contracts, ML inference, vision diagnosis, RAG anti-hallucination, and storage utilities:

```bash
pytest tests/unit/test_foundation.py -v
```

---

## 📚 Documentation Directory

- [docs/project_charter.md](docs/project_charter.md): Business objective, scope, SLAs, and requirements.
- [docs/architecture.md](docs/architecture.md): Complete architecture diagram and Medallion schema design.
- [docs/dataset_sources.md](docs/dataset_sources.md): Dataset registry, data.gov.in, AGMARKNET, and IMD specs.
- [docs/implementation_plan.md](docs/implementation_plan.md): 10-phase engineering roadmap.
- [docs/progress.md](docs/progress.md): Real-time implementation tracking, test logs, and blockers.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
