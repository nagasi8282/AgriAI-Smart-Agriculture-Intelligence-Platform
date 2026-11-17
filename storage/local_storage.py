"""
AgriAI Storage Layer - Local File Storage Provider
Manages local data lake storage with partitioned Bronze, Silver, and Gold directory layout.
"""

import os
import json
import shutil
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, List, Dict, Any
import pandas as pd

from backend.config.settings import settings


class LocalStorageProvider:
    """Provides local filesystem abstraction mimicking S3 object storage."""

    def __init__(self, base_dir: Optional[str] = None):
        self.base_dir = Path(base_dir or settings.DATA_DIR)
        self.raw_dir = Path(settings.RAW_DATA_DIR)
        self.processed_dir = Path(settings.PROCESSED_DATA_DIR)
        self.sample_dir = Path(settings.SAMPLE_DATA_DIR)
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self._ensure_directories()

    def _ensure_directories(self) -> None:
        """Create standard Medallion directories if not present."""
        for p in [self.base_dir, self.raw_dir, self.processed_dir, self.sample_dir, self.upload_dir]:
            p.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def compute_checksum(file_path: Path) -> str:
        """Calculate SHA-256 hash for data lineage and deduplication audit."""
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(65536), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def save_raw_record(self, domain: str, data: Any, filename: Optional[str] = None) -> Path:
        """
        Store raw data in Bronze layer partitioned by year and month.
        Path: data/raw/{domain}/year={YYYY}/month={MM}/{filename}
        """
        now = datetime.now(timezone.utc)
        partition_dir = self.raw_dir / domain / f"year={now.year}" / f"month={now.month:02d}"
        partition_dir.mkdir(parents=True, exist_ok=True)

        if not filename:
            filename = f"{domain}_{now.strftime('%Y%m%d_%H%M%S')}.json"

        target_path = partition_dir / filename

        if isinstance(data, pd.DataFrame):
            data.to_parquet(target_path.with_suffix(".parquet"), index=False)
            return target_path.with_suffix(".parquet")
        elif isinstance(data, (dict, list)):
            with open(target_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, default=str)
            return target_path
        elif isinstance(data, str):
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(data)
            return target_path
        elif isinstance(data, bytes):
            with open(target_path, "wb") as f:
                f.write(data)
            return target_path
        else:
            raise ValueError(f"Unsupported data type for raw storage: {type(data)}")

    def load_sample_dataset(self, domain: str) -> pd.DataFrame:
        """Load baseline sample dataset for development and testing."""
        csv_path = self.sample_dir / f"{domain}_ap_sample.csv"
        if not csv_path.exists():
            raise FileNotFoundError(f"Sample dataset not found at: {csv_path}")
        return pd.read_csv(csv_path)

    def list_raw_files(self, domain: str) -> List[Path]:
        """List all raw Bronze files for a specific data domain."""
        domain_dir = self.raw_dir / domain
        if not domain_dir.exists():
            return []
        return list(domain_dir.glob("**/*.*"))


local_storage = LocalStorageProvider()
