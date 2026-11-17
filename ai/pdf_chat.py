"""
AgriAI Generative AI - PDF Chat Interface Module
Provides high-level question answering interface over indexed agricultural documents.
"""

from typing import Dict, Any, Optional
from ai.rag_pipeline import rag_pipeline
from backend.schemas.ai import DocumentAskResponse


class AgriDocAIChat:
    """Interface connecting user questions to the grounded RAG pipeline."""

    @staticmethod
    def ask(query: str, document_id: Optional[str] = None, top_k: int = 3) -> DocumentAskResponse:
        return rag_pipeline.query(query=query, top_k=top_k, document_id=document_id)


pdf_chat = AgriDocAIChat()
