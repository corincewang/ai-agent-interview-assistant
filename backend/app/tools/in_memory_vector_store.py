import math
from uuid import UUID

from app.domain.models import (
    DocumentType,
    EmbeddedDocumentChunk,
    RetrievedKnowledgeChunk,
)


class InMemoryVectorStore:
    def __init__(self) -> None:
        self._chunks_by_session: dict[UUID, list[EmbeddedDocumentChunk]] = {}

    async def upsert_chunks(
        self,
        session_id: UUID,
        chunks: list[EmbeddedDocumentChunk],
    ) -> list[UUID]:
        existing_chunks = self._chunks_by_session.setdefault(session_id, [])
        existing_by_chunk_id = {item.chunk.id: item for item in existing_chunks}

        for chunk in chunks:
            existing_by_chunk_id[chunk.chunk.id] = chunk

        self._chunks_by_session[session_id] = list(existing_by_chunk_id.values())
        return [chunk.chunk.id for chunk in chunks]

    async def search(
        self,
        session_id: UUID,
        query_embedding: list[float],
        top_k: int,
        document_types: list[DocumentType] | None = None,
        filters: dict[str, object] | None = None,
    ) -> list[RetrievedKnowledgeChunk]:
        if top_k <= 0:
            return []

        candidates = self._chunks_by_session.get(session_id, [])
        scored_results: list[RetrievedKnowledgeChunk] = []

        for candidate in candidates:
            if document_types and not self._matches_document_type(candidate, document_types):
                continue
            if filters and not self._matches_filters(candidate, filters):
                continue

            scored_results.append(
                RetrievedKnowledgeChunk(
                    chunk=candidate.chunk,
                    score=_cosine_similarity(query_embedding, candidate.embedding),
                    rank=0,
                    retrieval_query="<embedding>",
                )
            )

        scored_results.sort(key=lambda result: result.score, reverse=True)
        return [
            RetrievedKnowledgeChunk(
                chunk=result.chunk,
                score=result.score,
                rank=index + 1,
                retrieval_query=result.retrieval_query,
            )
            for index, result in enumerate(scored_results[:top_k])
        ]

    def _matches_document_type(
        self,
        candidate: EmbeddedDocumentChunk,
        document_types: list[DocumentType],
    ) -> bool:
        document_type = candidate.chunk.metadata.get("document_type")
        return document_type in {item.value for item in document_types} or document_type in document_types

    def _matches_filters(
        self,
        candidate: EmbeddedDocumentChunk,
        filters: dict[str, object],
    ) -> bool:
        return all(candidate.chunk.metadata.get(key) == value for key, value in filters.items())


def _cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0

    dot_product = sum(left_value * right_value for left_value, right_value in zip(left, right))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))

    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0

    return dot_product / (left_norm * right_norm)
