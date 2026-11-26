# 🌾 AgriAI – Smart Agriculture Intelligence Platform

[![Python 3.12](https://img.shields.io/badge/Python-3.12-green.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111+-009688.svg)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B.svg)](https://streamlit.io/)
[![Zero--Cost Hosting](https://img.shields.io/badge/Deployment-Streamlit%20Cloud%20(%E2%82%B90%2Fmo)-brightgreen.svg)](docs/zero_cost_architecture.md)
[![Tests Passing](https://img.shields.io/badge/Tests-48%20Passing-success.svg)](docs/deployment_testing.md)
[![Architecture](https://img.shields.io/badge/Architecture-Medallion%20Lakehouse-blue.svg)](docs/architecture.md)
[![Target Region](https://img.shields.io/badge/Focus-Andhra%20Pradesh%20(India)-darkgreen.svg)](docs/project_charter.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An enterprise-grade, end-to-end Smart Agriculture Intelligence Platform integrating **Medallion Data Engineering (Bronze, Silver, Gold)**, **Cloud Warehousing (Snowflake & AWS S3)**, **Predictive Machine Learning (Yield & Price Forecasting with TreeSHAP)**, **Precision Fertilizer Recommendation (ANGRAU Stoichiometric Balancing)**, **Deep Learning Computer Vision (Plant Disease Diagnosis with Grad-CAM)**, and **Generative AI (AgriDoc AI PDF RAG with Page Citations)** tailored for **Andhra Pradesh, India**.

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
AI & MACHINE LEARNING LAYER (Random Forest + TreeSHAP | MobileNetV2 + Grad-CAM | Fertilizer Balancing)
         ↓
GENERATIVE AI LAYER (AgriAI Assistant & AgriDoc AI PDF RAG with Page Citations)
         ↓
PRESENTATION DASHBOARD (Modern Agrivision SaaS Streamlit UI with Interactive Plotly Visualizations)
```

For the complete technical blueprint and sequence diagrams, see [docs/architecture.md](docs/architecture.md).

---

## 🚀 Key Modules & Capabilities

1. **Dashboard Overview**: KPI cards, district coverage, live freshness badges, and agro-climatic summaries.
2. **Crop Intelligence**: Multi-year time-series exploration of AP crop area, production, and yield.
3. **Weather Intelligence**: District-level rainfall anomalies, temperature trends, and climate indicators.
4. **Mandi Price Intelligence**: AGMARKNET wholesale prices, trading spreads, and APMC yard comparisons.
5. **Soil & Fertilizer Support**: Soil Health Card nutrient classification, ML formulation selection, and transparent ANGRAU/ICAR commercial product bag scheduling.
6. **Crop Yield Prediction**: Machine learning regression estimating quintals/ha ($R^2 = 0.9926$) with TreeSHAP feature attributions.
7. **Mandi Price Forecasting**: Time-series regression model ($MAPE = 6.05\%$) projecting wholesale commodity prices.
8. **Plant Disease Detection**: Deep learning foliage classifier (MobileNetV2 / EfficientNetB0) generating Grad-CAM visual saliency heatmaps, guided by *Demilie (2024), Journal of Big Data*.
9. **AgriAI Assistant**: Conversational assistant grounded in regional agricultural datasets.
10. **AgriDoc AI (PDF RAG)**: Question-answering over uploaded agricultural literature with exact document and page citations ($[Document, Page]$) and anti-hallucination guardrails.
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
git clone https://github.com/nagasi8282/AgriAI-Smart-Agriculture-Intelligence-Platform.git
cd AgriAI-Smart-Agriculture-Intelligence-Platform

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

## 🌐 Zero-Cost Public Cloud Deployment (Streamlit Community Cloud)

AgriAI is pre-configured for **100% permanent free deployment ($0 / ₹0 monthly infrastructure cost)** on [Streamlit Community Cloud](https://share.streamlit.io):

1. **Sign in** to [share.streamlit.io](https://share.streamlit.io) with your GitHub account.
2. Click **New app** ➔ select repository `nagasi8282/AgriAI-Smart-Agriculture-Intelligence-Platform`.
3. Set **Branch**: `main`.
4. Set **Main file path**: `app/Home.py` *(Important: entry point is `app/Home.py`)*.
5. Click **Deploy!**.

For the complete zero-cost deployment blueprint and Azure safety audit, see:
- 📖 [Streamlit Cloud Deployment Guide](docs/streamlit_deployment.md)
- 🏗️ [Zero-Cost Architecture Blueprint](docs/zero_cost_architecture.md)
- 🛡️ [Azure Cost Safety & Verification Guide](docs/azure_cost_safety.md)

---

## 🧪 Running Automated Tests

AgriAI includes an extensive test suite verifying API contracts, ML inference, vision diagnosis, RAG anti-hallucination, storage utilities, and standalone zero-cost module execution:

```bash
pytest tests -v
```
*(**48 out of 48 tests passing** - 100% success rate)*.

---

## 📚 Documentation Directory

- [docs/deployment_audit.md](docs/deployment_audit.md): Complete project audit and cloud feasibility assessment.
- [docs/zero_cost_architecture.md](docs/zero_cost_architecture.md): Zero-cost architecture and dual-mode decoupling.
- [docs/streamlit_deployment.md](docs/streamlit_deployment.md): Step-by-step Streamlit Community Cloud guide.
- [docs/azure_cost_safety.md](docs/azure_cost_safety.md): Azure spending caps, budget alerts, and cost prevention.
- [docs/deployment_testing.md](docs/deployment_testing.md): Automated verification matrix across all 12 modules.
- [docs/troubleshooting.md](docs/troubleshooting.md): Common deployment errors and self-healing resolutions.
- [docs/project_charter.md](docs/project_charter.md): Business objective, scope, SLAs, and requirements.
- [docs/architecture.md](docs/architecture.md): Complete architecture diagram and Medallion schema design.
- [docs/dataset_sources.md](docs/dataset_sources.md): Dataset registry, data.gov.in, AGMARKNET, and IMD specs.
- [docs/ml_documentation.md](docs/ml_documentation.md): Detailed ML models, formulas, and evaluation benchmarks.

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
