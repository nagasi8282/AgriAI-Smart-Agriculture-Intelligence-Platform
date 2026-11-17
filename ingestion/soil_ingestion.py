"""
AgriAI Ingestion - Soil Health Connector
Ingests Soil Health Card district nutrient indices with biological plausibility validation.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import pandas as pd

from ingestion.common.base_connector import BaseIngestionConnector
from ingestion.common.validator import data_validator
from storage.local_storage import local_storage


class SoilHealthIngestionConnector(BaseIngestionConnector):
    """Ingestion connector for official Soil Health Card portal datasets."""

    def __init__(self):
        super().__init__(source_name="soil_health_card_moa", domain="soil")

    def extract(self, source_path: Optional[Path] = None, **kwargs) -> List[Dict[str, Any]]:
        """Extract soil health records from source survey files or sample baseline."""
        if source_path and Path(source_path).exists():
            df = pd.read_csv(source_path)
        else:
            df = local_storage.load_sample_dataset("soil_health")

        return df.to_dict(orient="records")

    def run_pipeline(self, source_path: Optional[Path] = None) -> Dict[str, Any]:
        """Execute full extraction, enrichment, validation, and Bronze landing."""
        self.logger.info("Starting soil health dataset ingestion...")

        raw_records = self.execute_with_retry(self.extract, source_path=source_path)
        if not raw_records:
            return {"status": "success", "rows_ingested": 0, "quarantined": 0}

        # 1. Validation & Quarantine Routing
        valid_records, rejected_records = data_validator.validate_soil(raw_records)

        quarantined_count = len(rejected_records)
        if quarantined_count > 0:
            q_path = data_validator.route_to_quarantine(self.domain, rejected_records)
            self.logger.warning(f"Quarantined {quarantined_count} invalid soil records to {q_path}")

        # 2. Bronze Metadata Injection
        enriched_records = [self.inject_bronze_metadata(r) for r in valid_records]

        # 3. Bronze Lake Storage Landing
        if enriched_records:
            bronze_path = local_storage.save_raw_record(
                domain=self.domain,
                data=enriched_records,
                filename=f"soil_health_ingest_{len(enriched_records)}.json"
            )
            self.logger.info(f"Landed {len(enriched_records)} soil records to Bronze layer: {bronze_path}")

        return {
            "status": "success",
            "domain": self.domain,
            "rows_extracted": len(raw_records),
            "rows_ingested": len(enriched_records),
            "quarantined": quarantined_count,
        }


soil_connector = SoilHealthIngestionConnector()
