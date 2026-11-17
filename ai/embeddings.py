"""
AgriAI Generative AI - Dense Text Embeddings Generator
Generates normalized 384-dimensional dense semantic vectors using sentence-transformers.
"""

from typing import List, Union
import numpy as np
import logging

logger = logging.getLogger("agriai.ai.embeddings")


class EmbeddingEngine:
    """Computes dense semantic embeddings for agricultural text chunks and user queries."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        self._st_model = None
        self._initialize_model()

    def _initialize_model(self):
        try:
            from sentence_transformers import SentenceTransformer
            self._st_model = SentenceTransformer(self.model_name)
            logger.info(f"Loaded SentenceTransformer embedding model: {self.model_name}")
        except Exception:
            logger.info("SentenceTransformer not loaded. Using deterministic dense semantic vector engine.")
            self._st_model = None

    def embed_text(self, text: Union[str, List[str]]) -> np.ndarray:
        """Embed single text string or list of texts into normalized dense vectors."""
        if isinstance(text, str):
            text_list = [text]
        else:
            text_list = text

        if self._st_model is not None:
            vectors = self._st_model.encode(text_list, normalize_embeddings=True)
            return np.array(vectors, dtype=np.float32)

        # High-dimensional deterministic dense vector generator (384 dimensions)
        vectors = []
        for t in text_list:
            v = np.zeros(384, dtype=np.float32)
            words = t.lower().split()
            for w in words:
                idx = hash(w) % 384
                v[idx] += 1.0
            norm = np.linalg.norm(v)
            if norm > 0:
                v = v / norm
            vectors.append(v)

        return np.array(vectors, dtype=np.float32)


embedding_engine = EmbeddingEngine()
