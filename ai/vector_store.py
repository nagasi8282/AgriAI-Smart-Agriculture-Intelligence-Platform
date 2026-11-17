"""
AgriAI Generative AI - Vector Store & Semantic Retrieval Index
Stores document vectors and executes cosine similarity searches with threshold filtering.
"""

from typing import List, Dict, Any, Tuple, Optional
import numpy as np
from ai.embeddings import embedding_engine


class AgriVectorStore:
    """In-memory dense vector index supporting cosine similarity search and metadata filtering."""

    def __init__(self):
        self._chunks: List[Dict[str, Any]] = []
        self._vectors: Optional[np.ndarray] = None

    def add_chunks(self, chunks: List[Dict[str, Any]]) -> int:
        """Embed text chunks and add to vector index."""
        if not chunks:
            return 0

        texts = [c["text"] for c in chunks]
        new_vectors = embedding_engine.embed_text(texts)

        if self._vectors is None or len(self._vectors) == 0:
            self._vectors = new_vectors
        else:
            self._vectors = np.vstack([self._vectors, new_vectors])

        self._chunks.extend(chunks)
        return len(chunks)

    def search(
        self,
        query: str,
        top_k: int = 4,
        document_id: Optional[str] = None,
        min_score: float = 0.25,
    ) -> List[Tuple[float, Dict[str, Any]]]:
        """
        Execute cosine similarity search against indexed document chunks.
        Returns list of (relevance_score, chunk_dict) sorted by score descending.
        """
        if self._vectors is None or len(self._chunks) == 0:
            return []

        query_vec = embedding_engine.embed_text(query)[0]

        # Compute cosine similarity: dot product of normalized vectors
        scores = np.dot(self._vectors, query_vec)

        results = []
        for idx, score in enumerate(scores):
            chunk = self._chunks[idx]
            if document_id and chunk["document_id"] != document_id:
                continue

            if float(score) >= min_score:
                results.append((float(score), chunk))

        results.sort(key=lambda x: x[0], reverse=True)
        return results[:top_k]

    def clear(self):
        """Reset index."""
        self._chunks = []
        self._vectors = None

    def __len__(self):
        return len(self._chunks)


vector_store = AgriVectorStore()
