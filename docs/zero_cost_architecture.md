# AgriAI Zero-Cost Architecture ($0 / ₹0 Monthly Infrastructure)

## 1. Architectural Blueprint

The AgriAI platform is designed to run in production with an **absolute zero-cost constraint**. 

```
                                  [ Public Internet Users ]
                                             |
                                             v
                           +-----------------------------------+
                           |   Streamlit Community Cloud       |
                           |   (Permanent Free Tier: $0/mo)    |
                           |   - 1 GB RAM, 1 vCPU              |
                           |   - Multi-page UI (app/Home.py)   |
                           +-----------------------------------+
                                             |
                     +-----------------------+-----------------------+
                     |                                               |
                     v                                               v
       +----------------------------+                 +----------------------------+
       |   Dual-Mode API Client     |                 |  Real-Time Open-Meteo API  |
       |  (app/utils/api_client.py) |                 | (api.open-meteo.com)       |
       |  - In-process service call |                 |  - Free, Public, Keyless   |
       |  - Fast, zero latency      |                 |  - Sub-second AP Weather   |
       +----------------------------+                 +----------------------------+
                     |
       +-------------+-------------+-------------+-------------+
       |                           |                           |
       v                           v                           v
+---------------+           +---------------+           +---------------+
| ML Prediction |           | Disease CV    |           | AgriDoc RAG   |
| Engine        |           | Engine        |           | Engine        |
| - Yield RF    |           | - MobileNetV2 |           | - Seeded Docs |
| - Price Reg   |           | - Grad-CAM    |           | - Dense 384d  |
| - Fertilizer  |           | - Pure PIL/NP |           | - Citations   |
+---------------+           +---------------+           +---------------+
       |                           |                           |
       +-------------+-------------+-------------+-------------+
                     |
                     v
       +----------------------------+
       |    Local Medallion Data    |
       | - Bronze/Silver Parquet    |
       | - Gold SQLite Mart (1.5MB) |
       | - Sample AP Datasets (CSV) |
       +----------------------------+
```

---

## 2. Zero-Cost Infrastructure Principles

### 2.1 Compute: Streamlit Community Cloud (Free)
- **Host**: [https://share.streamlit.io](https://share.streamlit.io)
- **Cost**: **$0 / ₹0 forever**.
- **Specs**: 1 GB RAM, 1 vCPU, automatic SSL certificate, global CDN.
- **Continuous Deployment**: Automatic redeployment upon every push to the `main` GitHub branch.

### 2.2 Microservice Decoupling: Dual-Mode Architecture
- Traditional multi-tier architectures require a separate cloud server (e.g. AWS EC2, Azure App Service, Render) running the FastAPI backend 24/7, which incurs monthly hosting costs.
- AgriAI employs a **Dual-Mode API Client** (`app/utils/api_client.py`):
  1. **HTTP Mode**: When deployed via Docker Compose or during local development, it communicates with FastAPI at `http://localhost:8000/api/v1`.
  2. **In-Process Standalone Mode**: When hosted on Streamlit Community Cloud, it automatically falls back to in-process execution of the backend services (`analytics_service`, `prediction_service`, `disease_service`, `rag_service`, `live_weather_service`).
  3. **Zero Hosting Overhead**: Eliminates the need to maintain, monitor, or pay for a separate backend server.

### 2.3 Storage: Medallion Lake + Embedded SQLite ($0)
- Instead of paying ₹2,500+/month for managed cloud databases (RDS, Cloud SQL, Azure PostgreSQL Flexible Server), AgriAI utilizes:
  - Local sample datasets (`data/sample/*.csv`) covering AP crop production, mandi prices, weather, and soil health.
  - An embedded SQLite dimensional warehouse (`data/agriai_warehouse.db`, 1.5 MB) storing standardized dimensions and fact tables.
  - Zero cloud ingress, egress, or storage volume charges.

### 2.4 Machine Learning Inference ($0)
- Trained models (`fertilizer_model.joblib`, `price_model_pipeline.joblib`, `yield_prediction_pipeline.joblib`) are version-controlled in the repository (< 5 MB total).
- Scikit-Learn pipelines execute on standard CPU in < 15 milliseconds without GPU requirements or cloud endpoints.

### 2.5 Computer Vision & Grad-CAM ($0)
- Disease detection runs a lightweight transfer-learning diagnostic pipeline with synthetic focal Grad-CAM saliency overlays.
- Operates purely in-memory using PIL and NumPy, bypassing heavy PyTorch GPU overhead and preventing out-of-memory crashes on free cloud containers.

### 2.6 AgriDoc AI RAG & Literature Search ($0)
- Seeded with peer-reviewed literature (Demilie 2024, ANGRAU guidelines) and deterministic 384-dimensional dense semantic vectors.
- Requires no paid OpenAI, Anthropic, or cloud vector database subscriptions.

---

## 3. Monthly Cost Breakdown

| Component | Provider / Tier | Monthly Cost (USD) | Monthly Cost (INR) |
| :--- | :--- | :--- | :--- |
| **Web UI Hosting** | Streamlit Community Cloud (Free) | $0.00 | ₹0.00 |
| **Backend Compute** | In-Process Dual Mode | $0.00 | ₹0.00 |
| **Database** | Embedded SQLite & Local Parquet | $0.00 | ₹0.00 |
| **ML Inference** | Local Scikit-Learn (CPU) | $0.00 | ₹0.00 |
| **Weather Telemetry** | Open-Meteo Public API | $0.00 | ₹0.00 |
| **Source Control & CI** | GitHub Public Repo + Actions | $0.00 | ₹0.00 |
| **SSL / HTTPS** | Streamlit Cloud Auto-SSL | $0.00 | ₹0.00 |
| **Total Monthly Bill** | — | **$0.00** | **₹0.00** |
