"""
AgriAI Backend - Analytics Router
Serves agricultural statistical datasets: Crop Production, Mandi Prices, Weather, Soil Health.
"""

from typing import List, Optional
from fastapi import APIRouter, Query
from backend.services.analytics_service import analytics_service
from backend.schemas.analytics import (
    DashboardSummary,
    CropProductionRecord,
    MandiPriceRecord,
    WeatherRecord,
    SoilRecord,
)

router = APIRouter(prefix="/analytics", tags=["Agricultural Analytics"])


@router.get("/summary", response_model=DashboardSummary)
async def get_dashboard_summary():
    """Get high-level agricultural KPIs and metrics for the dashboard."""
    return analytics_service.get_dashboard_summary()


@router.get("/crops", response_model=List[CropProductionRecord])
async def get_crop_production(
    district: Optional[str] = Query(None, description="Andhra Pradesh District name"),
    crop: Optional[str] = Query(None, description="Crop name, e.g. Paddy, Cotton, Chillies"),
    season: Optional[str] = Query(None, description="Season (Kharif, Rabi, Summer)"),
    year_start: Optional[int] = Query(None, description="Start year"),
    year_end: Optional[int] = Query(None, description="End year"),
):
    """Retrieve historical crop production, area, and yield statistics."""
    return analytics_service.get_crop_production(
        district=district,
        crop=crop,
        season=season,
        year_start=year_start,
        year_end=year_end,
    )


@router.get("/mandi-prices", response_model=List[MandiPriceRecord])
async def get_mandi_prices(
    district: Optional[str] = Query(None, description="District name"),
    market: Optional[str] = Query(None, description="APMC Market name"),
    commodity: Optional[str] = Query(None, description="Commodity name"),
):
    """Retrieve AGMARKNET wholesale mandi prices and arrivals."""
    return analytics_service.get_mandi_prices(
        district=district,
        market=market,
        commodity=commodity,
    )


@router.get("/weather", response_model=List[WeatherRecord])
async def get_weather(
    district: Optional[str] = Query(None, description="District name"),
):
    """Retrieve meteorological observations and temperature/rainfall trends."""
    return analytics_service.get_weather(district=district)


@router.get("/soil", response_model=List[SoilRecord])
async def get_soil(
    district: Optional[str] = Query(None, description="District name"),
):
    """Retrieve Soil Health Card nutrient ratings and pH measurements."""
    return analytics_service.get_soil(district=district)
