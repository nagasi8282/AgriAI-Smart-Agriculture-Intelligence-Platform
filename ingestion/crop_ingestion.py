"""
AgriAI Ingestion - Crop Production Connector
Ingests district-wise agricultural production datasets (DES / data.gov.in format)
with incremental watermarking, schema validation, and Bronze partitioning.
"""

from typing import Dict, Any, List, Optional
from pathlib import Path
import pandas as pd

from ingestion.common.base_connector import BaseIngestionConnector
from ingestion.common.watermark import watermark_manager
from ingestion.common.validator import data_validator
from storage.local_storage import local_storage
from backend.config.settings import settings


class CropProductionIngestionConnector(BaseIngestionConnector):
    """Ingestion connector for official Andhra Pradesh crop statistics."""

    def __init__(self):
        super().__init__(source_name="des_data_gov_in", domain="crop_production")

    def extract(self, source_path: Optional[Path] = None, full_load: bool = False) -> List[Dict[str, Any]]:
        """
        Extract records from local landing files or sample archive.
        Filters by watermark if full_load is False.
        """
        if source_path and Path(source_path).exists():
            df = pd.read_csv(source_path)
        else:
            df = local_storage.load_sample_dataset("crop_production")

        # Watermark filter
        if not full_load:
            last_watermark = watermark_manager.get_watermark(self.domain)
            if last_watermark:
                df = df[df["crop_year"] > int(last_watermark)]

        return df.to_dict(orient="records")

    def run_pipeline(self, source_path: Optional[Path] = None, full_load: bool = False) -> Dict[str, Any]:
        """Execute full extraction, enrichment, validation, and Bronze landing."""
        self.logger.info(f"Starting crop production ingestion (full_load={full_load})...")

        raw_records = self.execute_with_retry(self.extract, source_path=source_path, full_load=full_load)
        if not raw_records:
            self.logger.info("No new crop production records found to ingest.")
            return {"status": "success", "rows_ingested": 0, "quarantined": 0}

        # 1. Validation & Quarantine Routing
        valid_records, rejected_records = data_validator.validate_crop_production(raw_records)

        quarantined_count = len(rejected_records)
        if quarantined_count > 0:
            q_path = data_validator.route_to_quarantine(self.domain, rejected_records)
            self.logger.warning(f"Quarantined {quarantined_count} invalid crop production records to {q_path}")

        # 2. Bronze Metadata Injection
        enriched_records = [self.inject_bronze_metadata(r) for r in valid_records]

        # 3. Bronze Lake Storage Landing
        if enriched_records:
            bronze_path = local_storage.save_raw_record(
                domain=self.domain,
                data=enriched_records,
                filename=f"crop_production_ingest_{len(enriched_records)}.json"
            )
            self.logger.info(f"Landed {len(enriched_records)} records to Bronze layer: {bronze_path}")

            # 4. Advance High-Watermark
            max_year = max(r["crop_year"] for r in enriched_records)
            watermark_manager.update_watermark(
                domain=self.domain,
                watermark_column="crop_year",
                high_watermark=max_year,
                rows_ingested=len(enriched_records)
            )

        return {
            "status": "success",
            "domain": self.domain,
            "rows_extracted": len(raw_records),
            "rows_ingested": len(enriched_records),
            "quarantined": quarantined_count,
        }


crop_connector = CropProductionIngestionConnector()
