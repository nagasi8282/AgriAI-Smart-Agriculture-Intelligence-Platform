"""
AgriAI Backend - Assistant Router
Provides conversational intelligence endpoint with domain guardrails and context grounding.
"""

from fastapi import APIRouter
from backend.services.rag_service import rag_service
from backend.schemas.ai import ChatRequest, ChatResponse

router = APIRouter(prefix="/assistant", tags=["AgriAI Conversational Assistant"])


@router.post("/chat", response_model=ChatResponse)
async def chat_with_assistant(req: ChatRequest):
    """
    Conversational assistant for agricultural guidance across Andhra Pradesh.
    Integrates crop intelligence, mandi prices, and weather observations.
    """
    return rag_service.general_chat(
        message=req.message,
        district=req.district or "Guntur",
        crop=req.crop,
    )
