"""
AgriAI Machine Learning - Fertilizer Recommendation Model Evaluation
Computes precision, recall, F1-scores, accuracy, and confusion matrix
for the trained fertilizer recommendation classification pipeline.
"""

import os
import json
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "data", "sample", "fertilizer_recommendation_sample.csv")
MODEL_FILE = os.path.join(os.path.dirname(__file__), "..", "saved_models", "fertilizer_model.joblib")
METRICS_FILE = os.path.join(os.path.dirname(__file__), "..", "saved_models", "fertilizer_model_metrics.json")


def evaluate_fertilizer_model(data_path: str = DATA_PATH, model_path: str = MODEL_FILE, output_metrics: str = METRICS_FILE):
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}. Please train the model first.")
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found: {data_path}.")

    pipeline = joblib.load(model_path)
    df = pd.read_csv(data_path)

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

    _, X_test, _, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    y_pred = pipeline.predict(X_test)
    acc = float(accuracy_score(y_test, y_pred))
    report_dict = classification_report(y_test, y_pred, output_dict=True)
    labels = sorted(list(y.unique()))
    cm = confusion_matrix(y_test, y_pred, labels=labels).tolist()

    # Extract feature names & importances from RandomForest
    classifier = pipeline.named_steps["classifier"]
    preprocessor = pipeline.named_steps["preprocessor"]
    cat_encoder = preprocessor.named_transformers_["cat"]
    cat_feature_names = list(cat_encoder.get_feature_names_out(cat_cols))
    all_feature_names = cat_feature_names + num_cols
    importances = classifier.feature_importances_
    feat_imp = {feat: round(float(imp), 4) for feat, imp in zip(all_feature_names, importances)}
    top_features = dict(sorted(feat_imp.items(), key=lambda x: x[1], reverse=True)[:8])

    metrics = {
        "model_type": "RandomForestClassifier Pipeline",
        "test_accuracy": round(acc, 4),
        "macro_f1": round(report_dict["macro avg"]["f1-score"], 4),
        "weighted_f1": round(report_dict["weighted avg"]["f1-score"], 4),
        "test_samples": len(y_test),
        "classes": labels,
        "classification_report": report_dict,
        "confusion_matrix": cm,
        "top_feature_importances": top_features,
    }

    os.makedirs(os.path.dirname(output_metrics), exist_ok=True)
    with open(output_metrics, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    print(f"Evaluation complete. Test Accuracy: {acc * 100:.2f}%. Metrics written to {output_metrics}")
    return metrics


if __name__ == "__main__":
    evaluate_fertilizer_model()
