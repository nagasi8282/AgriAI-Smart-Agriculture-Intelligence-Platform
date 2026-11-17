"""
AgriAI Machine Learning - Mandi Price Prediction Model Training
Trains time-series aware regression models using rolling lag features and chronological split.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib

from backend.config.settings import settings
from storage.local_storage import local_storage

logger = logging.getLogger("agriai.ml.price_training")
MODEL_DIR = Path(settings.ML_MODEL_DIR)
MODEL_DIR.mkdir(parents=True, exist_ok=True)


def build_mandi_time_series_dataset() -> pd.DataFrame:
    """Load mandi price transactions and compute temporal lag and rolling features."""
    df = local_storage.load_sample_dataset("mandi_prices")
    df["arrival_date"] = pd.to_datetime(df["arrival_date"])
    df = df.sort_values(by=["market", "commodity", "arrival_date"]).reset_index(drop=True)

    # Feature Engineering: Lags & Rolling statistics per commodity-market series
    df["day_of_week"] = df["arrival_date"].dt.day_of_week
    df["month"] = df["arrival_date"].dt.month

    df["lag_1_price"] = df.groupby(["market", "commodity"])["modal_price_inr"].shift(1)
    df["lag_7_price"] = df.groupby(["market", "commodity"])["modal_price_inr"].shift(7)
    df["rolling_7_mean"] = (
        df.groupby(["market", "commodity"])["modal_price_inr"]
        .shift(1)
        .rolling(7, min_periods=1)
        .mean()
    )

    # Impute missing initial lags with baseline modal price
    df["lag_1_price"] = df["lag_1_price"].fillna(df["modal_price_inr"])
    df["lag_7_price"] = df["lag_7_price"].fillna(df["modal_price_inr"])
    df["rolling_7_mean"] = df["rolling_7_mean"].fillna(df["modal_price_inr"])

    return df


def train_price_models() -> Dict[str, Any]:
    """Train time-series price models with chronological validation."""
    df = build_mandi_time_series_dataset()

    categorical_features = ["market", "commodity"]
    numeric_features = ["day_of_week", "month", "lag_1_price", "lag_7_price", "rolling_7_mean", "arrival_tonnes"]
    target = "modal_price_inr"

    # Chronological Split: Train Jan-March, Test April 2024
    split_date = pd.Timestamp("2024-04-01")
    train_df = df[df["arrival_date"] < split_date]
    test_df = df[df["arrival_date"] >= split_date]

    X_train = train_df[categorical_features + numeric_features]
    y_train = train_df[target]
    X_test = test_df[categorical_features + numeric_features]
    y_test = test_df[target]

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features),
            ("num", StandardScaler(), numeric_features),
        ]
    )

    candidate_models = {
        "Ridge_Baseline": Ridge(alpha=1.0),
        "Random_Forest": RandomForestRegressor(n_estimators=100, max_depth=10, random_state=42),
    }

    results = {}
    best_model_name = None
    best_mae = float("inf")
    best_pipeline = None

    for name, model in candidate_models.items():
        pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("regressor", model)])
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100

        results[name] = {"MAE": round(mae, 2), "RMSE": round(rmse, 2), "MAPE": round(mape, 2)}
        print(f"Price Model [{name}]: MAE={mae:.2f}, RMSE={rmse:.2f}, MAPE={mape:.2f}%")

        if mae < best_mae:
            best_mae = mae
            best_model_name = name
            best_pipeline = pipeline

    artifact_path = MODEL_DIR / "price_model_pipeline.joblib"
    joblib.dump(best_pipeline, artifact_path)

    metadata_path = MODEL_DIR / "price_model_metadata.json"
    metadata = {
        "best_model": best_model_name,
        "evaluation_metrics": results,
        "split_date": "2024-04-01",
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "saved_at": pd.Timestamp.now().isoformat(),
    }
    with open(metadata_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, indent=2)

    print(f"Best Price Model [{best_model_name}] saved to {artifact_path}")
    return metadata


if __name__ == "__main__":
    train_price_models()
