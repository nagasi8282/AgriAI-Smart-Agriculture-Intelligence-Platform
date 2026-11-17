"""
AgriAI Machine Learning - Yield Prediction Evaluation Report
Generates out-of-time evaluation metrics, residual analysis, and per-crop performance tables.
"""

import json
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

from backend.config.settings import settings
from ml.yield_prediction.train import build_synthetic_training_dataset, MODEL_DIR


def evaluate_yield_pipeline() -> pd.DataFrame:
    """Evaluate trained model on the holdout test set (2022-2023)."""
    model_path = MODEL_DIR / "yield_prediction_pipeline.joblib"
    if not model_path.exists():
        raise FileNotFoundError(f"Trained model not found at: {model_path}. Please run train.py first.")

    model = joblib.load(model_path)
    df = build_synthetic_training_dataset()

    test_df = df[df["crop_year"] >= 2022].copy()
    features = [
        "district", "crop", "season", "area_hectares", "rainfall_mm",
        "temp_avg_c", "nitrogen_kg_ha", "phosphorus_kg_ha", "potassium_kg_ha", "soil_ph"
    ]
    X_test = test_df[features]
    y_test = test_df["yield_quintal_per_ha"]

    y_pred = model.predict(X_test)
    test_df["predicted_yield"] = y_pred
    test_df["residual_error"] = y_pred - y_test

    # Per-crop evaluation breakdown
    crop_metrics = []
    for crop_name, group in test_df.groupby("crop"):
        mae = mean_absolute_error(group["yield_quintal_per_ha"], group["predicted_yield"])
        rmse = np.sqrt(mean_squared_error(group["yield_quintal_per_ha"], group["predicted_yield"]))
        r2 = r2_score(group["yield_quintal_per_ha"], group["predicted_yield"])
        crop_metrics.append({
            "Crop": crop_name,
            "Test_Samples": len(group),
            "Mean_Actual_Yield": round(group["yield_quintal_per_ha"].mean(), 2),
            "Mean_Predicted_Yield": round(group["predicted_yield"].mean(), 2),
            "MAE": round(mae, 2),
            "RMSE": round(rmse, 2),
            "R2": round(r2, 4),
        })

    eval_df = pd.DataFrame(crop_metrics)
    eval_csv = MODEL_DIR / "yield_evaluation_breakdown.csv"
    eval_df.to_csv(eval_csv, index=False)
    print("--- Per-Crop Evaluation Report (Holdout Test 2022-2023) ---")
    print(eval_df.to_string(index=False))
    return eval_df


if __name__ == "__main__":
    evaluate_yield_pipeline()
