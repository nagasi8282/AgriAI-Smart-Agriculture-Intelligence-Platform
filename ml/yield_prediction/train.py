"""
AgriAI Machine Learning - Crop Yield Prediction Model Training
Trains ensemble regressors (RandomForest, GradientBoosting) using chronological train/test splitting
to avoid data leakage, evaluates MAE, RMSE, and R2, and saves the best model artifact.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Tuple
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib

from backend.config.settings import settings
from storage.local_storage import local_storage

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("agriai.ml.yield_training")

MODEL_DIR = Path(settings.ML_MODEL_DIR)
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def build_synthetic_training_dataset() -> pd.DataFrame:
    """
    Synthesize complete feature matrix combining crop production, meteorological,
    and soil health indicators for Andhra Pradesh districts.
    """
    crop_df = local_storage.load_sample_dataset("crop_production")
    soil_df = local_storage.load_sample_dataset("soil_health").set_index("district")
    weather_df = local_storage.load_sample_dataset("weather")

    # Aggregate average weather by district
    weather_summary = weather_df.groupby("district").agg({
        "rainfall_mm": "sum",
        "temp_mean_c": "mean",
    }).to_dict(orient="index")

    soil_dict = soil_df.to_dict(orient="index")

    rows = []
    for _, row in crop_df.iterrows():
        dist = row["district_name"]
        w = weather_summary.get(dist, {"rainfall_mm": 850.0, "temp_mean_c": 28.5})
        s = soil_dict.get(dist, {
            "available_nitrogen_kg_ha": 300.0,
            "available_phosphorus_kg_ha": 20.0,
            "available_potassium_kg_ha": 180.0,
            "soil_ph": 7.2,
        })

        rows.append({
            "district": dist,
            "crop": row["crop"],
            "season": row["season"],
            "crop_year": int(row["crop_year"]),
            "area_hectares": float(row["area_hectares"]),
            "rainfall_mm": float(w["rainfall_mm"]),
            "temp_avg_c": float(w["temp_mean_c"]),
            "nitrogen_kg_ha": float(s["available_nitrogen_kg_ha"]),
            "phosphorus_kg_ha": float(s["available_phosphorus_kg_ha"]),
            "potassium_kg_ha": float(s["available_potassium_kg_ha"]),
            "soil_ph": float(s["soil_ph"]),
            "yield_quintal_per_ha": float(row["yield_quintal_per_ha"]),
        })

    return pd.DataFrame(rows)


def train_yield_models() -> Dict[str, Any]:
    """Train and benchmark candidate regressors with chronological validation split."""
    logger.info("Loading agricultural feature dataset...")
    df = build_synthetic_training_dataset()

    categorical_features = ["district", "crop", "season"]
    numeric_features = [
        "area_hectares", "rainfall_mm", "temp_avg_c",
        "nitrogen_kg_ha", "phosphorus_kg_ha", "potassium_kg_ha", "soil_ph"
    ]
    target = "yield_quintal_per_ha"

    # Chronological Split: Train on <= 2021, Test on >= 2022 to avoid temporal leakage
    train_mask = df["crop_year"] <= 2021
    test_mask = df["crop_year"] >= 2022

    X_train = df.loc[train_mask, categorical_features + numeric_features]
    y_train = df.loc[train_mask, target]
    X_test = df.loc[test_mask, categorical_features + numeric_features]
    y_test = df.loc[test_mask, target]

    logger.info(f"Training partition (<=2021): {len(X_train)} samples | Test partition (2022-2023): {len(X_test)} samples")

    # Feature transformation preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", StandardScaler(), numeric_features),
        ]
    )

    candidate_models = {
        "Ridge_Baseline": Ridge(alpha=1.0),
        "Random_Forest": RandomForestRegressor(n_estimators=100, max_depth=12, random_state=42),
        "Gradient_Boosting": GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42),
    }

    results = {}
    best_model_name = None
    best_r2 = -float("inf")
    best_pipeline = None

    for name, model in candidate_models.items():
        pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("regressor", model)])
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)

        results[name] = {"MAE": round(mae, 3), "RMSE": round(rmse, 3), "R2": round(r2, 4)}
        logger.info(f"Model [{name}]: MAE={mae:.3f}, RMSE={rmse:.3f}, R²={r2:.4f}")

        if r2 > best_r2:
            best_r2 = r2
            best_model_name = name
            best_pipeline = pipeline

    # Save best model artifact and evaluation metadata
    artifact_path = MODEL_DIR / "yield_prediction_pipeline.joblib"
    joblib.dump(best_pipeline, artifact_path)

    metadata_path = MODEL_DIR / "yield_model_metadata.json"
    metadata = {
        "best_model": best_model_name,
        "evaluation_metrics": results,
        "features": {
            "categorical": categorical_features,
            "numeric": numeric_features,
        },
        "target": target,
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "saved_at": pd.Timestamp.now().isoformat(),
    }
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    logger.info(f"Best model [{best_model_name}] saved to {artifact_path}")
    return metadata


if __name__ == "__main__":
    train_yield_models()
