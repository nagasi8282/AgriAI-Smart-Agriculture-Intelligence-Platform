# AgriAI: Deployment & Infrastructure Guide

## 1. Local Development Setup

### 1.1 Python Virtual Environment
```bash
# 1. Create and activate virtual environment
python -m venv .venv

# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# Linux / macOS:
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure local environment variables
cp .env.example .env
```

### 1.2 Running Services Locally
```bash
# Terminal 1: Launch FastAPI Backend (Port 8000)
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Launch Streamlit Frontend (Port 8501)
streamlit run app/Home.py --server.port 8501
```
- Frontend: [http://localhost:8501](http://localhost:8501)
- Backend Docs (Swagger UI): [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)
- Health Check: [http://localhost:8000/health](http://localhost:8000/health)

---

## 2. Docker Compose Containerized Deployment

AgriAI provides a production-grade multi-container setup running PostgreSQL 16, FastAPI, and Streamlit:

```bash
# Build and launch all containers
docker-compose up --build -d

# Verify container health
docker-compose ps

# View container logs
docker-compose logs -f backend
```

### Container Port Mapping

| Service Name | Container Name | Internal Port | Host Port | Health Check |
| :--- | :--- | :--- | :--- | :--- |
| **PostgreSQL** | `agriai_postgres` | 5432 | 5432 | `pg_isready -U agriai_admin` |
| **FastAPI Backend** | `agriai_backend` | 8000 | 8000 | `curl -f http://localhost:8000/health` |
| **Streamlit Frontend** | `agriai_frontend` | 8501 | 8501 | HTTP 200 on `/` |

---

## 3. Cloud Infrastructure Integration

### 3.1 AWS S3 Cloud Object Storage
When running in Cloud mode, Bronze data lake files are directed to AWS S3:
1. Create an S3 bucket: `s3://agriai-data-lake-ap/`.
2. Configure IAM least-privilege policy allowing `s3:PutObject`, `s3:GetObject`, and `s3:ListBucket`.
3. Set environment variables in `.env`:
   ```env
   AWS_ACCESS_KEY_ID=AKIA...
   AWS_SECRET_ACCESS_KEY=...
   AWS_REGION=ap-south-1
   S3_BUCKET_NAME=agriai-data-lake-ap
   ```

### 3.2 Snowflake Cloud Data Warehouse
1. Execute initialization scripts in order:
   - `snowflake/01_setup.sql`: Creates `AGRIAI_WH`, `AGRIAI_DW`, schemas (`BRONZE_RAW`, `SILVER_STAGING`, `GOLD_MARTS`), and roles.
   - `snowflake/02_raw_tables.sql`: Creates raw tables for ingestion.
   - `snowflake/03_stages.sql`: Configures internal stages and external S3 stages.
   - `snowflake/04_warehouse_models.sql`: Deploys Gold dimensional star schema tables.
2. Run dbt transformations:
   ```bash
   cd dbt_agri
   dbt run --select staging
   dbt run --select marts
   dbt test
   ```

---

## 4. Production Checklist & Security Guidelines
- [x] Secrets and keys managed strictly via `.env` environment variables (no hardcoded credentials).
- [x] Input validation enforced via Pydantic schemas.
- [x] File upload size limits enforced (10 MB maximum for foliage images and PDFs).
- [x] Global exception handling preventing internal stack trace leaks to users.
- [x] CORS middleware configured for secure cross-origin requests.
