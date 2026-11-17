# AgriAI: Operational Runbook & System Administration

## 1. Document Control
- **Document Title**: AgriAI Platform Operational Runbook
- **Version**: 1.0.0
- **Reviewed Date**: November 2026
- **Target Audience**: Data Engineers, MLOps Engineers, System Administrators

---

## 2. Daily Pipeline Schedules & Airflow Orchestration

| Pipeline Job | Trigger Schedule | Orchestration Engine | SLA Target |
| :--- | :--- | :--- | :--- |
| **Mandi Price Ingestion** | 06:00 UTC / 11:30 AM IST Daily | Apache Airflow (`agri_daily_etl_pipeline`) | $\le 30$ mins |
| **Weather Ingestion** | Every 6 hours (`0 */6 * * *`) | Apache Airflow / Celery Executor | $\le 15$ mins |
| **Crop Production Update**| On-demand / Seasonal Release | Manual trigger / Scheduled Batch | $\le 60$ mins |
| **Silver & Gold Transformations**| Triggered on Bronze Landing | dbt Core (`dbt run`) | $\le 20$ mins |
| **Data Quality Assertions**| Post-Gold Mart Load | dbt test + Great Expectations | $\le 10$ mins |

---

## 3. Standard Operational Commands

### 3.1 Service Lifecycle Management
```bash
# Start all local development services (PostgreSQL, FastAPI, Streamlit)
docker-compose up -d

# Check real-time container health
docker-compose ps

# Restart backend after configuration update
docker-compose restart backend

# Stop all containers safely
docker-compose down
```

### 3.2 Running Data Pipelines & Ingestion Connectors
```bash
# Set PYTHONPATH and run full crop production ingestion
$env:PYTHONPATH="."; .venv\Scripts\python.exe -c "from ingestion.crop_ingestion import crop_connector; print(crop_connector.run_pipeline(full_load=True))"

# Run incremental mandi price ingestion
$env:PYTHONPATH="."; .venv\Scripts\python.exe -c "from ingestion.mandi_ingestion import mandi_connector; print(mandi_connector.run_pipeline())"

# Execute Bronze -> Silver -> Gold transformation
$env:PYTHONPATH="."; .venv\Scripts\python.exe -c "from backend.services.medallion_service import medallion_service; print(medallion_service.transform_bronze_to_silver()); print(medallion_service.transform_silver_to_gold())"
```

### 3.3 Running Automated Test Suites
```bash
# Run all unit, integration, and data quality tests
.venv\Scripts\pytest.exe tests -v

# Run only Medallion warehouse data quality tests
.venv\Scripts\pytest.exe tests/data_quality/test_medallion.py -v
```

---

## 4. Failure Handling, Retries & Quarantine Troubleshooting

### 4.1 Retry Strategy
All external data connectors implement exponential backoff:
- **Initial Delay**: 2 seconds.
- **Backoff Multiplier**: $2\times$ per failure.
- **Maximum Retries**: 3 attempts.
- **Failure Isolation**: Connector failures do not terminate unrelated pipeline tasks.

### 4.2 Inspecting Quarantined Anomalous Records
Records that violate business constraints (e.g. `min_price > max_price` or negative crop area) are routed to:
```
data/quarantine/{domain}/year={YYYY}/month={MM}/quarantine_{domain}_{timestamp}.json
```
To inspect quarantined records:
```bash
Get-ChildItem -Path data/quarantine -Recurse -Filter *.json | ForEach-Object {
    Write-Output "--- $($_.FullName) ---"
    Get-Content $_.FullName | ConvertFrom-Json | Select-Object -First 3
}
```

---

## 5. Machine Learning Retraining & Checkpoint Rollback

### 5.1 Retraining Policy
- **Yield Model**: Retrained annually upon official release of state-level crop statistics by the Directorate of Economics and Statistics.
- **Mandi Price Model**: Retrained monthly using the latest 90-day arrival and modal price records.
- **Vision Deep Learning**: Deep learning foliage models are **never** retrained automatically without human pathologist review and dataset validation.

### 5.2 Model Rollback Procedure
If a newly trained model exhibits regression in $R^2$ or elevated MAE:
```bash
# Check current metadata
Get-Content ml/saved_models/yield_model_metadata.json

# Restore previous checkpoint
Copy-Item ml/saved_models/yield_prediction_pipeline.joblib.bak ml/saved_models/yield_prediction_pipeline.joblib -Force
docker-compose restart backend
```
