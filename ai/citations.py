"""
AgriAI Generative AI - Citations Engine
Extracts verbatim snippets and constructs standardized bracketed page citations.
"""

from typing import Dict, Any, List
from backend.schemas.ai import Citation


class CitationEngine:
    """Manages passage extraction, scoring, and formal citation formatting."""

    @staticmethod
    def format_citation(
        document_name: str,
        page_number: int,
        chunk_index: int,
        score: float,
        text: str,
        max_snippet_len: int = 240,
    ) -> Citation:
        snippet = text[:max_snippet_len].strip() + ("..." if len(text) > max_snippet_len else "")
        return Citation(
            document_name=document_name,
            page_number=page_number,
            chunk_index=chunk_index,
            relevance_score=round(float(score), 3),
            verbatim_snippet=snippet,
        )

    @staticmethod
    def render_inline_citation(document_name: str, page_number: int) -> str:
        """Construct standard inline citation bracket."""
        return f"[Document: {document_name}, Page: {page_number}]"


citation_engine = CitationEngine()
