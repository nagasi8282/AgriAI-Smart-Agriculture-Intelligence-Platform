"""
AgriAI Backend - Disease Detection Router
Handles plant foliage image uploads and deep learning diagnostic inference with Grad-CAM heatmaps.
"""

from typing import Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from backend.services.disease_service import disease_service
from backend.schemas.disease import DiseasePredictionResponse

router = APIRouter(prefix="/disease", tags=["Plant Foliage Disease Detection"])


@router.post("/predict", response_model=DiseasePredictionResponse)
async def predict_foliage_disease(
    file: UploadFile = File(..., description="Plant foliage image file (JPEG or PNG)"),
    crop_hint: Optional[str] = Form(None, description="Optional crop hint (e.g. Tomato, Potato, Corn, Pepper)"),
):
    """
    Diagnose plant leaf pathologies using MobileNetV2 / EfficientNetB0 transfer learning.
    Returns predicted class, confidence, Grad-CAM saliency heatmap, and management guidelines.
    """
    if not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{file.content_type}'. Please upload an image file (JPEG, PNG)."
        )

    # Read image bytes
    contents = await file.read()
    if len(contents) > 10 * 1024 * 1024:  # 10 MB limit
        raise HTTPException(status_code=400, detail="File size exceeds maximum threshold (10 MB).")

    return disease_service.predict_image(contents, crop_hint=crop_hint)
