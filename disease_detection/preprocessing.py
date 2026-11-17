"""
AgriAI Computer Vision - Foliage Disease Preprocessing Pipeline
Implements image standardization, normalization, and training-only data augmentation.
Guided by: Demilie, W.B. (2024), Journal of Big Data, 11:71.
"""

from typing import Tuple, Optional
from PIL import Image, ImageOps, ImageEnhance
import numpy as np


class FoliageImagePreprocessor:
    """Preprocesses plant leaf images for MobileNetV2 and EfficientNetB0 backbones."""

    TARGET_SIZE: Tuple[int, int] = (224, 224)
    IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)

    @classmethod
    def preprocess_image(cls, image: Image.Image, is_training: bool = False) -> np.ndarray:
        """
        Resize, optionally augment (training set only), and normalize image.
        Strictly prevents data leakage by disabling augmentation during validation/testing.
        """
        # Ensure RGB format
        img = image.convert("RGB")

        # Training-only Data Augmentation
        if is_training:
            # 1. Random Horizontal Flip (50% probability)
            if np.random.rand() > 0.5:
                img = ImageOps.mirror(img)

            # 2. Random Vertical Flip (30% probability)
            if np.random.rand() > 0.7:
                img = ImageOps.flip(img)

            # 3. Slight Rotation (-15 to +15 degrees)
            angle = float(np.random.uniform(-15.0, 15.0))
            img = img.rotate(angle, resample=Image.Resampling.BILINEAR)

            # 4. Color Jitter (Brightness / Contrast within 10%)
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(float(np.random.uniform(0.9, 1.1)))

        # Standard Resize to 224x224
        img = img.resize(cls.TARGET_SIZE, resample=Image.Resampling.BILINEAR)

        # Convert to float numpy array normalized to [0, 1]
        arr = np.array(img, dtype=np.float32) / 255.0

        # Z-score normalization using standard ImageNet parameters
        normalized = (arr - cls.IMAGENET_MEAN) / cls.IMAGENET_STD

        # Transpose from (H, W, C) to (C, H, W) for PyTorch tensor conventions
        tensor_format = np.transpose(normalized, (2, 0, 1))
        return tensor_format

    @classmethod
    def denormalize_image(cls, tensor_format: np.ndarray) -> np.ndarray:
        """Reverse normalization for visual inspection and Grad-CAM blending."""
        arr = np.transpose(tensor_format, (1, 2, 0))
        denorm = (arr * cls.IMAGENET_STD) + cls.IMAGENET_MEAN
        clipped = np.clip(denorm * 255.0, 0, 255).astype(np.uint8)
        return clipped


preprocessor = FoliageImagePreprocessor()
