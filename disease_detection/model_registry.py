"""
AgriAI Computer Vision - Model Registry & Architecture Metadata
Tracks candidate architectures (MobileNetV2, EfficientNetB0), evaluation metrics,
parameter sizes, and literature benchmarks (Demilie, 2024).
"""

from typing import Dict, Any, List
from pathlib import Path

MODEL_REGISTRY: Dict[str, Dict[str, Any]] = {
    "MobileNetV2": {
        "architecture": "MobileNetV2",
        "description": "Depthwise separable convolutional network optimized for low-latency edge deployment.",
        "parameter_count_millions": 3.5,
        "input_resolution": (224, 224, 3),
        "target_classes_count": 12,
        "accuracy_benchmark_literature": 0.968,  # Reported in Demilie 2024 comparative survey
        "latency_cpu_ms": 48.0,
        "memory_footprint_mb": 14.2,
        "recommended_for": "Mobile field smartphones, Edge devices, Rythu Bharosa Kendra kiosks",
    },
    "EfficientNetB0": {
        "architecture": "EfficientNetB0",
        "description": "Compound scaled convolutional architecture balancing depth, width, and resolution.",
        "parameter_count_millions": 5.3,
        "input_resolution": (224, 224, 3),
        "target_classes_count": 12,
        "accuracy_benchmark_literature": 0.974,  # Reported in Demilie 2024 comparative survey
        "latency_cpu_ms": 76.0,
        "memory_footprint_mb": 21.5,
        "recommended_for": "Server-side batch diagnostics, Cloud GPU inference",
    },
}

DISEASE_CLASSES: List[Dict[str, str]] = [
    {"class": "Tomato___Early_blight", "crop": "Tomato", "condition": "Early Blight (Alternaria solani)"},
    {"class": "Tomato___Late_blight", "crop": "Tomato", "condition": "Late Blight (Phytophthora infestans)"},
    {"class": "Tomato___Bacterial_spot", "crop": "Tomato", "condition": "Bacterial Spot (Xanthomonas)"},
    {"class": "Tomato___healthy", "crop": "Tomato", "condition": "Healthy (Normal foliage vigor)"},
    {"class": "Potato___Early_blight", "crop": "Potato", "condition": "Early Blight (Alternaria solani)"},
    {"class": "Potato___Late_blight", "crop": "Potato", "condition": "Late Blight (Phytophthora infestans)"},
    {"class": "Potato___healthy", "crop": "Potato", "condition": "Healthy Foliage"},
    {"class": "Pepper__bell___Bacterial_spot", "crop": "Pepper Bell", "condition": "Bacterial Leaf Spot"},
    {"class": "Pepper__bell___healthy", "crop": "Pepper Bell", "condition": "Healthy Foliage"},
    {"class": "Corn_(maize)___Common_rust_", "crop": "Corn (Maize)", "condition": "Common Rust (Puccinia sorghi)"},
    {"class": "Corn_(maize)___Northern_Leaf_Blight", "crop": "Corn (Maize)", "condition": "Northern Leaf Blight"},
    {"class": "Corn_(maize)___healthy", "crop": "Corn (Maize)", "condition": "Healthy Foliage"},
]


class ModelRegistryManager:
    """Manages active models, class taxonomies, and literature comparison tables."""

    @staticmethod
    def get_model_specs(model_name: str = "MobileNetV2") -> Dict[str, Any]:
        return MODEL_REGISTRY.get(model_name, MODEL_REGISTRY["MobileNetV2"])

    @staticmethod
    def get_supported_classes() -> List[Dict[str, str]]:
        return DISEASE_CLASSES

    @staticmethod
    def get_comparative_table() -> List[Dict[str, Any]]:
        """Returns side-by-side architectural comparison for M.Tech academic reporting."""
        return list(MODEL_REGISTRY.values())


model_registry = ModelRegistryManager()
