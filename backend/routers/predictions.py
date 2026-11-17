"""
AgriAI Backend - Predictions Router
Serves Crop Yield, Mandi Price Forecasts, and Fertilizer Advisory Support.
"""

from fastapi import APIRouter
from backend.services.prediction_service import prediction_service
from backend.schemas.predictions import (
    YieldPredictionRequest,
    YieldPredictionResponse,
    PricePredictionRequest,
    PricePredictionResponse,
    FertilizerSupportRequest,
    FertilizerSupportResponse,
)

router = APIRouter(prefix="/predict", tags=["Predictive Machine Learning"])


@router.post("/yield", response_model=YieldPredictionResponse)
async def predict_crop_yield(req: YieldPredictionRequest):
    """Predict harvest yield (quintals/ha) and total production with SHAP feature attributions."""
    return prediction_service.predict_yield(req)


@router.post("/price", response_model=PricePredictionResponse)
async def predict_mandi_price(req: PricePredictionRequest):
    """Forecast mandi modal price (INR/quintal) for commodities across AP mandis."""
    return prediction_service.predict_price(req)


@router.post("/fertilizer", response_model=FertilizerSupportResponse)
async def recommend_fertilizers(req: FertilizerSupportRequest):
    """Generate transparent, rule-based fertilizer application schedules based on soil test inputs."""
    return prediction_service.recommend_fertilizer(req)
