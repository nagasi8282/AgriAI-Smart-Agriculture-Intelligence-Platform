"""
AgriAI Ingestion - Data Quality Validator & Quarantine Manager
Enforces domain constraints and routes malformed records to an isolated quarantine area.
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime, timezone
import pandas as pd

from backend.config.settings import settings


class DataQualityValidator:
    """Validates domain business rules and manages data quarantine for anomalous records."""

    def __init__(self, quarantine_dir: Optional[Path] = None):
        self.quarantine_dir = quarantine_dir or Path(settings.DATA_DIR) / "quarantine"
        self.quarantine_dir.mkdir(parents=True, exist_ok=True)

    def route_to_quarantine(self, domain: str, rejected_records: List[Dict[str, Any]]) -> Path:
        """Write rejected rows to partitioned quarantine store with rejection taxonomy."""
        now = datetime.now(timezone.utc)
        target_dir = self.quarantine_dir / domain / f"year={now.year}" / f"month={now.month:02d}"
        target_dir.mkdir(parents=True, exist_ok=True)

        filename = f"quarantine_{domain}_{now.strftime('%Y%m%d_%H%M%S')}.json"
        target_path = target_dir / filename

        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(rejected_records, f, indent=2, default=str)

        return target_path

    def validate_crop_production(self, records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Validate crop production records for non-negative area, production, and valid years."""
        valid, rejected = [], []
        for r in records:
            reasons = []
            if float(r.get("area_hectares", 0.0)) <= 0:
                reasons.append("Area in hectares must be positive.")
            if float(r.get("production_tonnes", 0.0)) < 0:
                reasons.append("Production in tonnes cannot be negative.")
            if not (2000 <= int(r.get("crop_year", 0)) <= 2030):
                reasons.append("Crop year out of realistic bounds (2000-2030).")

            if reasons:
                rej = dict(r)
                rej["_rejection_reasons"] = reasons
                rej["_quarantined_at"] = datetime.now(timezone.utc).isoformat()
                rejected.append(rej)
            else:
                valid.append(r)

        return valid, rejected

    def validate_mandi_prices(self, records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Validate AGMARKNET mandi prices enforcing min_price <= modal_price <= max_price."""
        valid, rejected = [], []
        for r in records:
            reasons = []
            min_p = float(r.get("min_price_inr", 0.0))
            mod_p = float(r.get("modal_price_inr", 0.0))
            max_p = float(r.get("max_price_inr", 0.0))

            if min_p <= 0 or mod_p <= 0 or max_p <= 0:
                reasons.append("Commodity prices must be positive non-zero values.")
            if not (min_p <= mod_p <= max_p):
                reasons.append(f"Price band violation: expected min ({min_p}) <= modal ({mod_p}) <= max ({max_p}).")

            if reasons:
                rej = dict(r)
                rej["_rejection_reasons"] = reasons
                rej["_quarantined_at"] = datetime.now(timezone.utc).isoformat()
                rejected.append(rej)
            else:
                valid.append(r)

        return valid, rejected

    def validate_weather(self, records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Validate meteorological observations for temperature range and valid humidity."""
        valid, rejected = [], []
        for r in records:
            reasons = []
            t_max = float(r.get("temp_max_c", 0.0))
            t_min = float(r.get("temp_min_c", 0.0))
            rain = float(r.get("rainfall_mm", 0.0))
            hum = float(r.get("relative_humidity_pct", 0.0))

            if t_min > t_max:
                reasons.append(f"Temperature anomaly: min ({t_min}°C) > max ({t_max}°C).")
            if rain < 0:
                reasons.append("Rainfall cannot be negative.")
            if not (0.0 <= hum <= 100.0):
                reasons.append(f"Relative humidity out of bounds (0-100%): {hum}%.")

            if reasons:
                rej = dict(r)
                rej["_rejection_reasons"] = reasons
                rej["_quarantined_at"] = datetime.now(timezone.utc).isoformat()
                rejected.append(rej)
            else:
                valid.append(r)

        return valid, rejected

    def validate_soil(self, records: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
        """Validate soil health parameters for biological plausibility."""
        valid, rejected = [], []
        for r in records:
            reasons = []
            ph = float(r.get("soil_ph", 7.0))
            n = float(r.get("available_nitrogen_kg_ha", 0.0))
            p = float(r.get("available_phosphorus_kg_ha", 0.0))
            k = float(r.get("available_potassium_kg_ha", 0.0))

            if not (3.5 <= ph <= 10.5):
                reasons.append(f"Soil pH value out of agricultural bounds (3.5-10.5): {ph}.")
            if n < 0 or p < 0 or k < 0:
                reasons.append("Primary soil nutrients (NPK) cannot be negative.")

            if reasons:
                rej = dict(r)
                rej["_rejection_reasons"] = reasons
                rej["_quarantined_at"] = datetime.now(timezone.utc).isoformat()
                rejected.append(rej)
            else:
                valid.append(r)

        return valid, rejected


data_validator = DataQualityValidator()
