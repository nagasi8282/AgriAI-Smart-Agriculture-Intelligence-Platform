from typing import List, Optional
from pydantic import BaseModel, Field
from datetime import date


class CropProductionFilter(BaseModel):
    state: Optional[str] = "Andhra Pradesh"
    district: Optional[str] = None
    crop: Optional[str] = None
    season: Optional[str] = None
    year_start: Optional[int] = None
    year_end: Optional[int] = None


class CropProductionRecord(BaseModel):
    state_name: str
    district_name: str
    crop_year: int
    season: str
    crop: str
    area_hectares: float
    production_tonnes: float
    yield_quintal_per_ha: float


class MandiPriceRecord(BaseModel):
    state: str
    district: str
    market: str
    commodity: str
    variety: str
    arrival_date: str
    min_price_inr: float
    max_price_inr: float
    modal_price_inr: float
    arrival_tonnes: Optional[float] = None


class WeatherRecord(BaseModel):
    district: str
    date: str
    temp_max_c: float
    temp_min_c: float
    temp_mean_c: float
    rainfall_mm: float
    relative_humidity_pct: float
    wind_speed_kmh: float
    is_forecast: bool = False
    condition: Optional[str] = "Normal"


class SoilRecord(BaseModel):
    district: str
    soil_type: str
    available_nitrogen_kg_ha: float
    available_phosphorus_kg_ha: float
    available_potassium_kg_ha: float
    soil_ph: float
    organic_carbon_pct: float
    electrical_conductivity_dsm: float
    nitrogen_category: Optional[str] = "Medium"
    phosphorus_category: Optional[str] = "Medium"
    potassium_category: Optional[str] = "Medium"


class DashboardSummary(BaseModel):
    total_crop_records: int
    total_districts: int
    total_crops_tracked: int
    latest_mandi_update: str
    weather_alert_count: int
    districts_list: List[str]
    crops_list: List[str]
