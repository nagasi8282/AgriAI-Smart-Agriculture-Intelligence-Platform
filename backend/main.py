"""
AgriAI Backend - FastAPI Application Entry Point
Production-grade REST microservice orchestrating data analytics, ML serving,
deep learning computer vision, and Generative AI RAG pipelines.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config.settings import settings
from backend.routers import (
    health_router,
    analytics_router,
    predictions_router,
    disease_router,
    assistant_router,
    documents_router,
)

# Configure structured logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("agriai.backend")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager for resource initialization and teardown."""
    logger.info(f"Initializing {settings.PROJECT_NAME} v{settings.VERSION}")
    logger.info(f"Runtime Environment: {settings.APP_ENV} | Debug: {settings.DEBUG}")
    logger.info(f"Target Primary Region: {settings.DEFAULT_STATE} (Districts: {len(settings.district_list)})")
    yield
    logger.info("Gracefully shutting down AgriAI backend services.")


# Instantiate FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=(
        "**AgriAI**: End-to-End Smart Agriculture Intelligence Platform for Andhra Pradesh.\n\n"
        "Features:\n"
        "- **Data Analytics**: Crop production history, AGMARKNET mandi prices, IMD weather trends, Soil health indices.\n"
        "- **Predictive Machine Learning**: Crop yield estimation with SHAP, mandi modal price forecasting.\n"
        "- **Deep Learning Vision**: Plant foliage disease diagnosis with Grad-CAM heatmaps (MobileNetV2 / EfficientNetB0).\n"
        "- **Generative AI & RAG**: AgriDoc AI question-answering with exact document page citations.\n"
    ),
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)

# CORS Middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict to specific domains in cloud production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handler to prevent leaking internal stack traces
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled exception at {request.url.path}: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": "An internal server error occurred. Please contact the system administrator.",
        },
    )

# Include Routers
app.include_router(health_router)
app.include_router(analytics_router, prefix=settings.API_V1_STR)
app.include_router(predictions_router, prefix=settings.API_V1_STR)
app.include_router(disease_router, prefix=settings.API_V1_STR)
app.include_router(assistant_router, prefix=settings.API_V1_STR)
app.include_router(documents_router, prefix=settings.API_V1_STR)


@app.get("/", tags=["Root"])
async def root():
    """Root entry point providing discovery links."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs_url": f"{settings.API_V1_STR}/docs",
        "health_check": f"{settings.API_V1_STR}/health",
        "target_region": settings.DEFAULT_STATE,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host=settings.BACKEND_HOST,
        port=settings.BACKEND_PORT,
        reload=settings.DEBUG,
    )
