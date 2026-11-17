"""
AgriAI Generative AI - Page-Aware Semantic Text Chunker
Splits agricultural documents into overlapping chunks while preserving page metadata.
"""

from typing import List, Dict, Any


class PageAwareChunker:
    """Splits text into overlapping chunks while attaching page metadata to every chunk."""

    def __init__(self, chunk_size: int = 600, chunk_overlap: int = 100):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_pages(
        self,
        document_id: str,
        document_name: str,
        pages: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Chunk text page-by-page preserving structural page references.
        Returns list of chunks with complete lineage metadata.
        """
        chunks = []
        global_chunk_idx = 0

        for page in pages:
            page_num = page["page_number"]
            page_text = page.get("text", "").strip()

            if not page_text:
                continue

            # Split text by sliding window
            start = 0
            text_len = len(page_text)

            while start < text_len:
                end = min(start + self.chunk_size, text_len)
                chunk_str = page_text[start:end].strip()

                if len(chunk_str) > 30:  # Skip tiny residual fragments
                    chunk_id = f"{document_id}_p{page_num}_c{global_chunk_idx}"
                    chunks.append({
                        "chunk_id": chunk_id,
                        "document_id": document_id,
                        "document_name": document_name,
                        "page_number": page_num,
                        "chunk_index": global_chunk_idx,
                        "text": chunk_str,
                        "char_count": len(chunk_str),
                    })
                    global_chunk_idx += 1

                if end >= text_len:
                    break
                start += (self.chunk_size - self.chunk_overlap)

        return chunks


chunker = PageAwareChunker()
