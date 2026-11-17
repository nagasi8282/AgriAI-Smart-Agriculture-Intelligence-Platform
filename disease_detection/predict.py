"""
AgriAI Computer Vision - Foliage Disease Predictor & Visual Explainer
Performs convolutional classification with Grad-CAM visual attention overlays.
"""

from typing import Dict, Any, Optional
from PIL import Image
import numpy as np

from disease_detection.preprocessing import preprocessor
from disease_detection.model_registry import model_registry
from backend.services.disease_service import disease_service


class FoliageDiseasePredictor:
    """Predictor wrapper for deep learning plant pathology inference."""

    def __init__(self, default_architecture: str = "MobileNetV2"):
        self.architecture = default_architecture
        self.classes = model_registry.get_supported_classes()

    def predict_image(self, image: Image.Image, crop_hint: Optional[str] = None) -> Dict[str, Any]:
        """
        Preprocess image, execute convolutional inference, and return diagnosis with Grad-CAM heatmap.
        """
        import io
        buf = io.BytesIO()
        image.save(buf, format="JPEG")
        buf.seek(0)

        response = disease_service.predict_image(buf.getvalue(), crop_hint=crop_hint)
        return response.dict()


disease_predictor = FoliageDiseasePredictor()
