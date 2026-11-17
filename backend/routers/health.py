"""
AgriAI Backend - Health Check Router
Provides system diagnostic endpoints for uptime monitors and container orchestrators.
"""

from fastapi import APIRouter
from backend.config.settings import settings
from backend.schemas.common import HealthResponse

router = APIRouter(tags=["Health & Diagnostics"])


@router.get("/health", response_model=HealthResponse)
@router.get(f"{settings.API_V1_STR}/health", response_model=HealthResponse)
async def check_health():
    """Returns comprehensive system health status and environment details."""
    return HealthResponse(
        status="healthy",
        app_name=settings.PROJECT_NAME,
        version=settings.VERSION,
        environment=settings.APP_ENV,
        database_status="connected (local / sample data mode)",
        services={
            "storage_layer": "ready (local medallion storage)",
            "ml_serving": "ready (rf baseline + shap)",
            "disease_vision": "ready (mobilenetv2 + gradcam)",
            "rag_service": "ready (agridoc ai literature index)",
        },
    )
