"""
AgriAI Frontend - REST API Client Helper
Handles resilient HTTP requests from Streamlit to the FastAPI backend.
"""

import os
import requests
from typing import Dict, Any, Optional, List

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
API_V1 = f"{BACKEND_URL}/api/v1"


class AgriAPIClient:
    """Centralized API client for all Streamlit modules."""

    @staticmethod
    def get_health() -> Dict[str, Any]:
        try:
            resp = requests.get(f"{BACKEND_URL}/health", timeout=3)
            return resp.json() if resp.status_code == 200 else {"status": "unhealthy"}
        except Exception:
            return {"status": "unreachable"}

    @staticmethod
    def get_dashboard_summary() -> Dict[str, Any]:
        try:
            resp = requests.get(f"{API_V1}/analytics/summary", timeout=5)
            return resp.json() if resp.status_code == 200 else {}
        except Exception:
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
            resp = requests.get(f"{API_V1}/analytics/crops", params=params, timeout=5)
            return resp.json() if resp.status_code == 200 else []
        except Exception:
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
            resp = requests.get(f"{API_V1}/analytics/mandi-prices", params=params, timeout=5)
            return resp.json() if resp.status_code == 200 else []
        except Exception:
            return []

    @staticmethod
    def get_weather(district: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {}
        if district and district != "All":
            params["district"] = district
        try:
            resp = requests.get(f"{API_V1}/analytics/weather", params=params, timeout=5)
            return resp.json() if resp.status_code == 200 else []
        except Exception:
            return []

    @staticmethod
    def get_soil(district: Optional[str] = None) -> List[Dict[str, Any]]:
        params = {}
        if district and district != "All":
            params["district"] = district
        try:
            resp = requests.get(f"{API_V1}/analytics/soil", params=params, timeout=5)
            return resp.json() if resp.status_code == 200 else []
        except Exception:
            return []

    @staticmethod
    def predict_yield(payload: Dict[str, Any]) -> Dict[str, Any]:
        try:
            resp = requests.post(f"{API_V1}/predict/yield", json=payload, timeout=5)
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
            resp = requests.post(f"{API_V1}/predict/price", json=payload, timeout=5)
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
            resp = requests.post(f"{API_V1}/predict/fertilizer", json=payload, timeout=5)
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
            resp = requests.post(f"{API_V1}/disease/predict", files=files, data=data, timeout=10)
            return resp.json() if resp.status_code == 200 else {"error": resp.text}
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    def chat_assistant(message: str, district: str = "Guntur", crop: Optional[str] = None) -> Dict[str, Any]:
        try:
            payload = {"message": message, "district": district, "crop": crop}
            resp = requests.post(f"{API_V1}/assistant/chat", json=payload, timeout=10)
            return resp.json() if resp.status_code == 200 else {"response": "Error reaching assistant."}
        except Exception as e:
            return {"response": f"Connection error: {e}"}

    @staticmethod
    def ask_document(query: str, document_id: Optional[str] = None) -> Dict[str, Any]:
        try:
            payload = {"query": query, "document_id": document_id}
            resp = requests.post(f"{API_V1}/documents/ask", json=payload, timeout=10)
            return resp.json() if resp.status_code == 200 else {"answer": "Error querying document."}
        except Exception as e:
            return {"answer": f"Connection error: {e}"}

    @staticmethod
    def list_documents() -> List[Dict[str, Any]]:
        try:
            resp = requests.get(f"{API_V1}/documents", timeout=5)
            return resp.json() if resp.status_code == 200 else []
        except Exception:
            return []


api_client = AgriAPIClient()
