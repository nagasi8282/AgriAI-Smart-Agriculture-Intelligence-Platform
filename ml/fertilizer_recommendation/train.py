"""
AgriAI Machine Learning - Fertilizer Formulation Classifier Training
Trains a Random Forest classification pipeline on regional soil and crop parameters
to recommend optimal fertilizer formulation blends for Andhra Pradesh agriculture.
"""

import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "sample", "fertilizer_recommendation_sample.csv")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "saved_models")
MODEL_FILE = os.path.join(MODEL_DIR, "fertilizer_model.joblib")


def train_fertilizer_model(data_path: str = DATA_PATH, model_save_path: str = MODEL_FILE):
    """Train and persist the fertilizer recommendation classification pipeline."""
    if not os.path.exists(data_path):
        from ml.fertilizer_recommendation.dataset import generate_fertilizer_dataset
        generate_fertilizer_dataset(num_samples=1500, output_path=data_path)

    df = pd.read_csv(data_path)
    print(f"Loaded {len(df)} samples for fertilizer recommendation training.")

    cat_cols = ["crop", "soil_type"]
    num_cols = [
        "nitrogen_kg_ha",
        "phosphorus_kg_ha",
        "potassium_kg_ha",
        "soil_ph",
        "organic_carbon_pct",
        "moisture_pct",
    ]
    target_col = "recommended_formulation"

    X = df[cat_cols + num_cols]
    y = df[target_col]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    preprocessor = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), cat_cols),
            ("num", StandardScaler(), num_cols),
        ]
    )

    clf = RandomForestClassifier(
        n_estimators=120,
        max_depth=12,
        min_samples_split=4,
        random_state=42,
        n_jobs=-1,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", clf),
        ]
    )

    print("Training Random Forest Classifier for fertilizer formulation...")
    pipeline.fit(X_train, y_train)

    # Evaluate
    y_pred = pipeline.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"Test Accuracy: {acc * 100:.2f}%")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))

    os.makedirs(model_save_path if os.path.isdir(model_save_path) else os.path.dirname(model_save_path), exist_ok=True)
    joblib.dump(pipeline, model_save_path)
    print(f"Fertilizer recommendation model pipeline saved -> {model_save_path}")
    return pipeline, acc


if __name__ == "__main__":
    train_fertilizer_model()
