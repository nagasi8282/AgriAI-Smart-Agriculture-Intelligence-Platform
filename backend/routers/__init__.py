from backend.routers.health import router as health_router
from backend.routers.analytics import router as analytics_router
from backend.routers.predictions import router as predictions_router
from backend.routers.disease import router as disease_router
from backend.routers.assistant import router as assistant_router
from backend.routers.documents import router as documents_router

__all__ = [
    "health_router",
    "analytics_router",
    "predictions_router",
    "disease_router",
    "assistant_router",
    "documents_router",
]
