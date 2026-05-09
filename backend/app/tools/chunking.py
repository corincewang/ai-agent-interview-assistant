from uuid import uuid4

from app.domain.models import DocumentChunk, ParsedDocument


class RecursiveTextChunkingTool:
    def __init__(self, chunk_size: int = 900, chunk_overlap: int = 120) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    async def chunk_document(self, document: ParsedDocument) -> list[DocumentChunk]:
        text = document.raw_text.strip()
        if not text:
            return []

        chunks: list[DocumentChunk] = []
        start = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            boundary = self._find_boundary(text, start, end)
            chunk_text = text[start:boundary].strip()

            if chunk_text:
                chunks.append(
                    DocumentChunk(
                        id=uuid4(),
                        document_id=document.id,
                        text=chunk_text,
                        metadata={
                            "document_type": document.document_type.value,
                            "start_char": start,
                            "end_char": boundary,
                            "chunk_index": len(chunks),
                        },
                    )
                )

            if boundary >= len(text):
                break

            start = max(boundary - self.chunk_overlap, 0)

        return chunks

    def _find_boundary(self, text: str, start: int, proposed_end: int) -> int:
        if proposed_end >= len(text):
            return len(text)

        window = text[start:proposed_end]
        for separator in ("\n\n", "\n", "。", ".", " "):
            index = window.rfind(separator)
            if index > self.chunk_size // 2:
                return start + index + len(separator)

        return proposed_end

