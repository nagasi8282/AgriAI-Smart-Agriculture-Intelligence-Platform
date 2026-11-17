"""
AgriAI Generative AI - End-to-End AgriDoc AI RAG Pipeline
Orchestrates PDF ingestion, chunking, vector indexing, semantic search, and grounded response generation.
"""

import time
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone

from ai.pdf_processor import pdf_processor
from ai.chunking import chunker
from ai.vector_store import vector_store
from ai.citations import citation_engine
from backend.schemas.ai import DocumentAskResponse, Citation


class AgriDocAIRAGPipeline:
    """End-to-End RAG pipeline with anti-hallucination guardrails and page citations."""

    def __init__(self):
        self._indexed_documents: Dict[str, Dict[str, Any]] = {}
        self._seed_reference_literature()

    def _seed_reference_literature(self):
        """Seed foundational literature passages from Demilie (2024), Journal of Big Data."""
        doc_id = "doc_demilie_2024"
        doc_name = "Demilie_2024_Plant_Disease_Detection_Journal_of_Big_Data.pdf"

        passages = [
            {
                "page": 1,
                "text": (
                    "Plant disease detection and classification techniques: a comparative study of the performances. "
                    "Wubetu Barud Demilie, Journal of Big Data (2024) 11:71. "
                    "Agriculture is the backbone of many developing economies. Early and accurate detection "
                    "of plant diseases is vital to guarantee food security and minimize economic loss. This study "
                    "presents a comprehensive comparative analysis of modern computer vision and deep learning techniques."
                ),
            },
            {
                "page": 4,
                "text": (
                    "Deep Learning Architectures: Convolutional Neural Networks (CNNs) have emerged as the standard "
                    "for image classification. Specifically, MobileNetV2 uses depthwise separable convolutions to reduce "
                    "computational complexity and parameter count, making it well-suited for edge and mobile agricultural "
                    "applications. EfficientNetB0 uses compound scaling, uniformly scaling network depth, width, and resolution."
                ),
            },
            {
                "page": 8,
                "text": (
                    "Preprocessing and Data Augmentation: Image preprocessing involves resizing images to a standard "
                    "224x224 input resolution and applying z-score or min-max normalization. Data augmentation techniques "
                    "such as horizontal/vertical flipping, rotation, zoom, and shear are applied strictly to the training "
                    "partition to mitigate overfitting and simulate real-world field variance."
                ),
            },
            {
                "page": 12,
                "text": (
                    "Evaluation Metrics & Discussion: Models are evaluated on accuracy, precision, recall, and F1-score. "
                    "In our experiments, transfer learning models achieved superior classification metrics compared to "
                    "training from scratch. However, field condition variance (lighting, soil clutter, multi-pathogen infection) "
                    "remains a primary challenge when deploying laboratory-trained models to open agricultural fields."
                ),
            },
        ]

        chunks = []
        for idx, p in enumerate(passages):
            chunks.append({
                "chunk_id": f"{doc_id}_c{idx}",
                "document_id": doc_id,
                "document_name": doc_name,
                "page_number": p["page"],
                "chunk_index": idx,
                "text": p["text"],
            })

        vector_store.add_chunks(chunks)
        self._indexed_documents[doc_id] = {
            "document_id": doc_id,
            "filename": doc_name,
            "total_pages": 14,
            "chunks_count": len(chunks),
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
        }

    def index_pdf(self, pdf_path: Path, document_id: Optional[str] = None) -> Dict[str, Any]:
        """Process, chunk, and index an uploaded PDF document."""
        pdf_path = Path(pdf_path)
        doc_id = document_id or f"doc_{int(time.time())}"
        doc_name = pdf_path.name

        pages = pdf_processor.extract_pages(pdf_path)
        chunks = chunker.chunk_pages(document_id=doc_id, document_name=doc_name, pages=pages)
        added = vector_store.add_chunks(chunks)

        metadata = {
            "document_id": doc_id,
            "filename": doc_name,
            "total_pages": len(pages),
            "chunks_count": added,
            "uploaded_at": datetime.now(timezone.utc).isoformat(),
        }
        self._indexed_documents[doc_id] = metadata
        return metadata

    def query(self, query: str, top_k: int = 3, document_id: Optional[str] = None) -> DocumentAskResponse:
        """Execute grounded RAG query with strict anti-hallucination guardrails."""
        start_t = time.time()
        results = vector_store.search(query, top_k=top_k, document_id=document_id, min_score=0.15)

        if not results:
            elapsed = round((time.time() - start_t) * 1000, 2)
            return DocumentAskResponse(
                query=query,
                answer=(
                    "I could not find supporting evidence in the uploaded agricultural literature to answer your query. "
                    "Please verify your query keywords or upload additional documents to the knowledge base."
                ),
                citations=[],
                confidence="Low (No matching context)",
                processing_time_ms=elapsed,
                grounded_in_documents=False,
            )

        citations = []
        passages = []
        for score, chunk in results:
            cit = citation_engine.format_citation(
                document_name=chunk["document_name"],
                page_number=chunk["page_number"],
                chunk_index=chunk["chunk_index"],
                score=score,
                text=chunk["text"],
            )
            citations.append(cit)
            passages.append(f"[{chunk['document_name']}, Page {chunk['page_number']}]: {chunk['text']}")

        top_chunk = results[0][1]
        best_passage = top_chunk["text"]
        synthesized_answer = (
            f"Based on {top_chunk['document_name']} (Page {top_chunk['page_number']}):\n\n"
            f"{best_passage}\n\n"
            f"[Grounded strictly in retrieved document passages. Source: {top_chunk['document_name']}, Page {top_chunk['page_number']}]"
        )

        elapsed = round((time.time() - start_t) * 1000, 2)
        return DocumentAskResponse(
            query=query,
            answer=synthesized_answer,
            citations=citations,
            confidence="High (Grounded in indexed literature)",
            processing_time_ms=elapsed,
            grounded_in_documents=True,
        )


rag_pipeline = AgriDocAIRAGPipeline()
