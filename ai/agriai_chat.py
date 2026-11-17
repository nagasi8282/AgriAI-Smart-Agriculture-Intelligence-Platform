"""
AgriAI Generative AI - Conversational Agriculture Assistant
Provides domain-grounded conversational responses with regional agronomic context for Andhra Pradesh.
"""

from typing import Dict, Any, Optional, List
from backend.services.rag_service import rag_service
from backend.schemas.ai import ChatRequest, ChatResponse


class AgriAIChatAssistant:
    """Conversational assistant managing multi-turn dialogue with agricultural domain guardrails."""

    def __init__(self):
        self.default_state = "Andhra Pradesh"

    def respond(self, message: str, district: str = "Guntur", crop: Optional[str] = None) -> ChatResponse:
        """Process natural language agricultural queries."""
        return rag_service.general_chat(message=message, district=district, crop=crop)


agriai_chat = AgriAIChatAssistant()
