from typing import List, Optional, Dict
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class ChatMessage(BaseModel):
    role: str = Field(..., description="'user', 'assistant', or 'system'")
    content: str


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    district: Optional[str] = "Guntur"
    crop: Optional[str] = None
    chat_history: Optional[List[ChatMessage]] = []


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    retrieved_context_used: bool = False
    source_domains: List[str] = []
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class Citation(BaseModel):
    document_name: str
    page_number: int
    chunk_index: int
    relevance_score: float
    verbatim_snippet: str


class DocumentAskRequest(BaseModel):
    query: str
    document_id: Optional[str] = None
    top_k: int = Field(default=4, ge=1, le=10)


class DocumentAskResponse(BaseModel):
    query: str
    answer: str
    citations: List[Citation]
    confidence: str
    processing_time_ms: float
    grounded_in_documents: bool = True
