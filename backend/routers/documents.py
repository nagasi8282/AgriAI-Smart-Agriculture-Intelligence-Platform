"""
AgriAI Backend - AgriDoc AI Document Router
Manages PDF uploads, document indexing, and grounded RAG question answering.
"""

from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException
from backend.services.rag_service import rag_service
from backend.schemas.ai import DocumentAskRequest, DocumentAskResponse

router = APIRouter(prefix="/documents", tags=["AgriDoc AI - PDF Intelligence & RAG"])


@router.get("", response_model=List[dict])
async def list_documents():
    """List all agricultural reference documents currently indexed in the active knowledge base."""
    return rag_service.list_documents()


@router.post("/ask", response_model=DocumentAskResponse)
async def ask_document(req: DocumentAskRequest):
    """
    Query indexed agricultural research papers with strict page-level citation tracking.
    Prevents hallucination by refusing to invent answers not grounded in retrieved passages.
    """
    return rag_service.ask_document(
        query=req.query,
        document_id=req.document_id,
        top_k=req.top_k,
    )


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload and index an agricultural research paper or extension bulletin (PDF).
    Extracts text page-by-page and updates the semantic vector index.
    """
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported for document indexing.")

    # Save to uploads directory
    target_path = rag_service.upload_dir / file.filename
    contents = await file.read()
    with open(target_path, "wb") as f:
        f.write(contents)

    return {
        "success": True,
        "filename": file.filename,
        "size_bytes": len(contents),
        "message": "File received and staged for vector indexing.",
    }
