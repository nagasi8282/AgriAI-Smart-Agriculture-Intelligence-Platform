from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field


class YieldPredictionRequest(BaseModel):
    state: str = Field(default="Andhra Pradesh")
    district: str = Field(..., description="Target district, e.g. Guntur")
    crop: str = Field(..., description="Target crop, e.g. Paddy (Rice)")
    season: str = Field(default="Kharif", description="Agricultural season (Kharif, Rabi, Summer)")
    crop_year: int = Field(default=2024, ge=2000, le=2030)
    area_hectares: float = Field(..., gt=0, description="Cultivated land area in hectares")
    rainfall_mm: Optional[float] = Field(default=850.0, ge=0)
    temp_avg_c: Optional[float] = Field(default=28.5, ge=5, le=50)
    nitrogen_kg_ha: Optional[float] = Field(default=320.0, ge=0)
    phosphorus_kg_ha: Optional[float] = Field(default=22.0, ge=0)
    potassium_kg_ha: Optional[float] = Field(default=180.0, ge=0)
    soil_ph: Optional[float] = Field(default=7.2, ge=3.5, le=10.5)


class YieldPredictionResponse(BaseModel):
    predicted_yield_quintal_per_ha: float
    estimated_total_production_tonnes: float
    model_version: str
    model_algorithm: str
    feature_importance: Dict[str, float]
    prediction_confidence_interval: Dict[str, float]
    disclaimer: str


class PricePredictionRequest(BaseModel):
    state: str = Field(default="Andhra Pradesh")
    district: str = Field(..., description="APMC district, e.g. Guntur")
    market: str = Field(..., description="APMC market yard name, e.g. Guntur")
    commodity: str = Field(..., description="Commodity name, e.g. Chilli, Cotton, Paddy")
    variety: Optional[str] = "Common"
    forecast_horizon_days: int = Field(default=7, ge=1, le=30)


class PricePredictionResponse(BaseModel):
    commodity: str
    market: str
    current_modal_price: float
    predicted_modal_price: float
    price_change_pct: float
    forecast_horizon_days: int
    historical_price_trend: List[Dict[str, float]]
    model_version: str
    disclaimer: str


class FertilizerSupportRequest(BaseModel):
    crop: str = Field(..., description="Cultivated crop name")
    district: str = Field(..., description="Location district")
    nitrogen: float = Field(..., ge=0, description="Available Soil N in kg/ha")
    phosphorus: float = Field(..., ge=0, description="Available Soil P in kg/ha")
    potassium: float = Field(..., ge=0, description="Available Soil K in kg/ha")
    soil_ph: float = Field(..., ge=3.5, le=10.5, description="Soil pH value")
    soil_type: Optional[str] = "Black Cotton"
    farm_area_acres: Optional[float] = Field(default=2.5, ge=0.1, le=500.0, description="Farm area in acres")
    farm_area_hectares: Optional[float] = Field(default=None, ge=0.05, le=200.0, description="Farm area in hectares")
    organic_carbon_pct: Optional[float] = Field(default=0.55, ge=0.05, le=3.0, description="Soil Organic Carbon %")
    moisture_pct: Optional[float] = Field(default=45.0, ge=5.0, le=95.0, description="Soil Moisture %")


class FertilizerSupportResponse(BaseModel):
    crop: str
    soil_type: Optional[str] = "Black Cotton"
    farm_area_acres: Optional[float] = 2.5
    farm_area_hectares: Optional[float] = 1.01
    recommended_blend: Optional[str] = "Urea + DAP + MOP"
    ml_confidence_pct: Optional[float] = 92.0
    nutrient_status: Dict[str, str]  # e.g. {"Nitrogen (N)": "Low (Deficient)"}
    target_rdf_kg_ha: Optional[Dict[str, float]] = None
    adjusted_rdf_kg_ha: Optional[Dict[str, float]] = None
    recommended_fertilizers: List[Dict[str, Any]]
    fertilizer_products: Optional[List[Dict[str, Any]]] = None
    total_50kg_bags: Optional[float] = None
    application_schedule: List[str]
    soil_amendment_advice: Optional[str] = None
    micronutrients: Optional[List[str]] = None
    organic_matter_advice: Optional[str] = None
    advisory_disclaimer: str
    model_version: Optional[str] = "1.0.0-rf-agronomic"
