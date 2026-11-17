"""
AgriAI Machine Learning - Mandi Price Prediction Inference Engine
Provides price forecasting using the trained time-series regression pipeline.
"""

from pathlib import Path
from typing import Dict, Any, List
import pandas as pd
import joblib

from backend.config.settings import settings

MODEL_PATH = Path(settings.ML_MODEL_DIR) / "price_model_pipeline.joblib"


class PricePredictionInference:
    def __init__(self):
        self._model = None
        self._load_model()

    def _load_model(self):
        if MODEL_PATH.exists():
            try:
                self._model = joblib.load(MODEL_PATH)
            except Exception:
                self._model = None

    def predict_price(self, features: Dict[str, Any]) -> float:
        """Run inference on input features."""
        if self._model is None:
            self._load_model()

        if self._model is not None:
            input_df = pd.DataFrame([features])
            pred = self._model.predict(input_df)[0]
            return float(max(0.0, round(pred, 2)))

        # Fallback benchmark
        benchmarks = {"Chillies": 18500.0, "Cotton": 6900.0, "Paddy": 2250.0, "Groundnut": 6300.0}
        return benchmarks.get(features.get("commodity", "Paddy"), 3000.0)


price_predictor = PricePredictionInference()
