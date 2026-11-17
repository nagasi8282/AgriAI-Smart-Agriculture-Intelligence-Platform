"""
AgriAI Ingestion - Watermark Manager
Tracks incremental extraction state across agricultural pipelines to prevent duplicate loads.
"""

import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timezone
from backend.config.settings import settings


class WatermarkManager:
    """Manages high-watermark tracking for incremental batch pipelines."""

    def __init__(self, state_file: Optional[Path] = None):
        self.state_file = state_file or Path(settings.DATA_DIR) / "watermarks.json"
        self._state: Dict[str, Dict[str, Any]] = {}
        self._load_state()

    def _load_state(self) -> None:
        """Load persistent watermark registry from disk."""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    self._state = json.load(f)
            except Exception:
                self._state = {}
        else:
            self._state = {}

    def _save_state(self) -> None:
        """Persist state to disk safely."""
        self.state_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(self._state, f, indent=2)

    def get_watermark(self, domain: str) -> Optional[Any]:
        """Retrieve current high-watermark value for a specific domain."""
        return self._state.get(domain, {}).get("high_watermark")

    def update_watermark(self, domain: str, watermark_column: str, high_watermark: Any, rows_ingested: int) -> None:
        """Advance high-watermark after successful pipeline completion."""
        self._state[domain] = {
            "watermark_column": watermark_column,
            "high_watermark": str(high_watermark),
            "last_updated_at": datetime.now(timezone.utc).isoformat(),
            "rows_ingested": rows_ingested,
        }
        self._save_state()

    def reset_watermark(self, domain: str) -> None:
        """Reset watermark to force full re-extraction."""
        if domain in self._state:
            del self._state[domain]
            self._save_state()


watermark_manager = WatermarkManager()
