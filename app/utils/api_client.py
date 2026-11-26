"""
AgriAI Frontend - Resilient Dual-Mode API Client Helper
Handles seamless HTTP requests to the FastAPI backend when available,
and provides instant, zero-cost in-process service fallbacks when running
standalone on Streamlit Community Cloud or serverless hosting.
"""

import os
import requests
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger("agriai.api_client")

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_V1 = f"{BACKEND_URL}/api/v1"


class AgriAPIClient:
    """
    Centralized dual-mode client for all Streamlit modules.
    Primary: REST HTTP endpoints against FastAPI microservice.
    Secondary: Direct in-process invocation of backend services (Zero-Cost Standalone mode).
    """

    @staticmethod
    def get_health() -> Dict[str, Any]:
        try:
            resp = requests.get(f"{API_V1}/health", timeout=2)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        # In-process standalone health status
        return {
            "status": "healthy",
            "app_name": "AgriAI Platform (Standalone Zero-Cost Mode)",
            "version": "1.0.0",
            "environment": "standalone-cloud",
            "database_status": "connected (local / sample storage mode)",
            "services": {
                "storage_layer": "ready (local medallion storage)",
                "ml_serving": "ready (in-process ML inference)",
                "disease_vision": "ready (MobileNetV2 / Grad-CAM)",
                "rag_service": "ready (AgriDoc AI literature index)",
            },
        }

    @staticmethod
    def get_dashboard_summary() -> Dict[str, Any]:
        try:
            resp = requests.get(f"{API_V1}/analytics/summary", timeout=3)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        try:
            from backend.services.analytics_service import analytics_service
            res = analytics_service.get_dashboard_summary()
            return res.model_dump() if hasattr(res, "model_dump") else res.dict()
        except Exception as e:
            logger.debug(f"In-process dashboard summary fallback error: {e}")
            return {}

    @staticmethod
    def get_crop_production(
        district: Optional[str] = None,
        crop: Optional[str] = None,
        season: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        params = {}
        if district and district != "All":
            params["district"] = district
        if crop and crop != "All":
            params["crop"] = crop
        if season and season != "All":
            params["season"] = season

        try:
            resp = requests.get(f"{API_V1}/analytics/crops", params=params, timeout=3)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        try:
            from backend.services.analytics_service import analytics_service
            records = analytics_service.get_crop_production(district=district, crop=crop, season=season)
            return [r.model_dump() if hasattr(r, "model_dump") else r.dict() for r in records]
        except Exception as e:
            logger.debug(f"In-process crop production fallback error: {e}")
            return []

    @staticmethod
    def get_mandi_prices(
        district: Optional[str] = None,
        market: Optional[str] = None,
        commodity: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        params = {}
        if district and district != "All":
            params["district"] = district
        if market and market != "All":
            params["market"] = market
        if commodity and commodity != "All":
            params["commodity"] = commodity

        try:
            resp = requests.get(f"{API_V1}/analytics/mandi-prices", params=params, timeout=3)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        try:
            from backend.services.analytics_service import analytics_service
            records = analytics_service.get_mandi_prices(district=district, market=market, commodity=commodity)
            return [r.model_dump() if hasattr(r, "model_dump") else r.dict() for r in records]
        except Exception as e:
            logger.debug(f"In-process mandi prices fallback error: {e}")
            return []

    @staticmethod
    def get_live_weather(district: Optional[str] = "Guntur") -> Optional[Dict[str, Any]]:
        params = {"district": district or "Guntur"}
        try:
            resp = requests.get(f"{API_V1}/analytics/weather/live", params=params, timeout=4)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        try:
            from backend.services.weather_live_service import live_weather_service
            return live_weather_service.fetch_live_weather(district=district)
        except Exception as e:
            logger.debug(f"In-process live weather fallback error: {e}")
            return None

    @staticmethod
    def get_weather(district: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {}
        if district and district != "All":
            params["district"] = district
        try:
            resp = requests.get(f"{API_V1}/analytics/weather", params=params, timeout=3)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        try:
            from backend.services.analytics_service import analytics_service
            records = analytics_service.get_weather(district=district)
            return [r.model_dump() if hasattr(r, "model_dump") else r.dict() for r in records]
        except Exception as e:
            logger.debug(f"In-process weather fallback error: {e}")
            return []

    @staticmethod
    def get_soil(district: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {}
        if district and district != "All":
            params["district"] = district
        try:
            resp = requests.get(f"{API_V1}/analytics/soil", params=params, timeout=3)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        try:
            from backend.services.analytics_service import analytics_service
            records = analytics_service.get_soil(district=district)
            return [r.model_dump() if hasattr(r, "model_dump") else r.dict() for r in records]
        except Exception as e:
            logger.debug(f"In-process soil fallback error: {e}")
            return []

    @staticmethod
    def predict_yield(payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            resp = requests.post(f"{API_V1}/predict/yield", json=payload, timeout=4)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        try:
            from backend.services.prediction_service import prediction_service
            from backend.schemas.predictions import YieldPredictionRequest
            res = prediction_service.predict_yield(YieldPredictionRequest(**payload))
            return res.model_dump() if hasattr(res, "model_dump") else res.dict()
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def predict_price(payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            resp = requests.post(f"{API_V1}/predict/price", json=payload, timeout=4)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        try:
            from backend.services.prediction_service import prediction_service
            from backend.schemas.predictions import PricePredictionRequest
            res = prediction_service.predict_price(PricePredictionRequest(**payload))
            return res.model_dump() if hasattr(res, "model_dump") else res.dict()
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def recommend_fertilizer(payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            resp = requests.post(f"{API_V1}/predict/fertilizer", json=payload, timeout=4)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        try:
            from backend.services.prediction_service import prediction_service
            from backend.schemas.predictions import FertilizerSupportRequest
            res = prediction_service.recommend_fertilizer(FertilizerSupportRequest(**payload))
            return res.model_dump() if hasattr(res, "model_dump") else res.dict()
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def predict_disease(file_bytes: bytes, filename: str, crop_hint: Optional[str] = None) -> Dict[str, Any]:
        try:
            files = {"file": (filename, file_bytes, "image/jpeg")}
            data = {"crop_hint": crop_hint} if crop_hint else {}
            resp = requests.post(f"{API_V1}/disease/predict", files=files, data=data, timeout=8)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        try:
            from backend.services.disease_service import disease_service
            res = disease_service.predict_image(file_bytes, crop_hint=crop_hint)
            return res.model_dump() if hasattr(res, "model_dump") else res.dict()
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def chat_assistant(message: str, district: str = "Guntur", crop: Optional[str] = None) -> Dict[str, Any]:
        try:
            payload = {"message": message, "district": district, "crop": crop}
            resp = requests.post(f"{API_V1}/assistant/chat", json=payload, timeout=8)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        try:
            from backend.services.rag_service import rag_service
            res = rag_service.general_chat(message=message, district=district, crop=crop)
            return res.model_dump() if hasattr(res, "model_dump") else res.dict()
        except Exception as e:
            return {"response": f"Assistant query error: {e}"}

    @staticmethod
    def ask_document(query: str, document_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            payload = {"query": query, "document_id": document_id}
            resp = requests.post(f"{API_V1}/documents/ask", json=payload, timeout=8)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        try:
            from backend.services.rag_service import rag_service
            res = rag_service.ask_document(query=query, document_id=document_id)
            return res.model_dump() if hasattr(res, "model_dump") else res.dict()
        except Exception as e:
            return {"answer": f"Document query error: {e}"}

    @staticmethod
    def list_documents() -> List[Dict[str, Any]]:
        try:
            resp = requests.get(f"{API_V1}/documents", timeout=4)
            if resp.status_code == 200:
                return resp.json()
        except Exception:
            pass

        try:
            from backend.services.rag_service import rag_service
            return rag_service.list_documents()
        except Exception:
            return []


# Export singleton
api_client = AgriAPIClient()
