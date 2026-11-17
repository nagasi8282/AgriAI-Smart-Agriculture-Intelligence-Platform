"""
AgriAI Computer Vision - Transfer Learning Training Pipeline
Harness for fine-tuning MobileNetV2 and EfficientNetB0 on plant pathology datasets.
Literature reference: Demilie (2024), Journal of Big Data.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any
from disease_detection.model_registry import model_registry
from disease_detection.evaluate import compare_candidate_models
from backend.config.settings import settings

logger = logging.getLogger("agriai.cv.training")
REGISTRY_DIR = Path(settings.MODEL_REGISTRY_DIR)
REGISTRY_DIR.mkdir(parents=True, exist_ok=True)


def run_transfer_learning_experiment() -> Dict[str, Any]:
    """
    Executes comparative transfer learning benchmark between MobileNetV2 and EfficientNetB0.
    Stores evaluation metrics and comparative table in the model registry.
    """
    logger.info("Initializing transfer learning comparative experiment...")
    comp_df = compare_candidate_models()

    output_path = REGISTRY_DIR / "transfer_learning_comparison.json"
    summary = {
        "benchmark_literature": "Demilie (2024), Journal of Big Data, 11:71",
        "models_evaluated": ["MobileNetV2", "EfficientNetB0"],
        "comparison_results": comp_df.to_dict(orient="records"),
        "field_generalization_note": (
            "Field performance in Andhra Pradesh open-canopy farms may vary due to solar glare, "
            "dust occlusion, and multi-disease coinfections compared to controlled laboratory benchmarks."
        ),
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    logger.info(f"Transfer learning benchmark completed. Report saved to {output_path}")
    return summary


if __name__ == "__main__":
    run_transfer_learning_experiment()
