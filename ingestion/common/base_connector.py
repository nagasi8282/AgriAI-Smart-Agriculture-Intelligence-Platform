"""
AgriAI Ingestion - Base Data Connector
Abstract connector providing structured metadata injection, retry policies,
cryptographic hashing, and error logging across all agricultural data pipelines.
"""

import time
import uuid
import hashlib
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

from storage.local_storage import local_storage

logger = logging.getLogger("agriai.ingestion")


class BaseIngestionConnector(ABC):
    """Abstract base connector establishing contract for all agricultural ingestion pipelines."""

    def __init__(self, source_name: str, domain: str):
        self.source_name = source_name
        self.domain = domain
        self.logger = logging.getLogger(f"agriai.ingestion.{domain}")

    def inject_bronze_metadata(self, record: Dict[str, Any], batch_id: Optional[str] = None) -> Dict[str, Any]:
        """Attach lineage metadata required by the Bronze Medallion specification."""
        enriched = dict(record)
        enriched["_ingest_id"] = str(uuid.uuid4())
        enriched["_batch_id"] = batch_id or str(uuid.uuid4())
        enriched["_source_system"] = self.source_name
        enriched["_ingested_at"] = datetime.now(timezone.utc).isoformat()
        return enriched

    @staticmethod
    def calculate_record_checksum(payload: Any) -> str:
        """Compute SHA-256 fingerprint for duplicate detection and lineage audit."""
        content = str(payload).encode("utf-8")
        return hashlib.sha256(content).hexdigest()

    def execute_with_retry(self, func, max_retries: int = 3, backoff_seconds: float = 2.0, *args, **kwargs):
        """Execute extraction function with exponential backoff retry logic."""
        last_exception = None
        for attempt in range(1, max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                self.logger.warning(
                    f"Extraction attempt {attempt}/{max_retries} failed for {self.source_name}: {e}. "
                    f"Retrying in {backoff_seconds}s..."
                )
                time.sleep(backoff_seconds)
                backoff_seconds *= 2

        self.logger.error(f"Extraction permanently failed for {self.source_name} after {max_retries} attempts.")
        raise last_exception

    @abstractmethod
    def extract(self, **kwargs) -> Any:
        """Extract data from upstream source (API, CSV, Database, or Stream)."""
        pass

    @abstractmethod
    def run_pipeline(self, **kwargs) -> Dict[str, Any]:
        """Execute full extraction, enrichment, validation, and Bronze landing."""
        pass
