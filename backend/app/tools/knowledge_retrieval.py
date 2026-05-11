from dataclasses import replace
from typing import Any
from uuid import UUID

from app.domain.models import (
    DocumentType,
    KnowledgeRetrievalResult,
)
from app.ports.tools import EmbeddingProvider, VectorStore


class DefaultKnowledgeRetrievalTool:
    def __init__(
        self,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ) -> None:
        self._embedding_provider = embedding_provider
        self._vector_store = vector_store

    async def retrieve_knowledge(
        self,
        session_id: UUID,
        query: str,
        top_k: int,
        document_types: list[DocumentType] | None = None,
        filters: dict[str, Any] | None = None,
    ) -> KnowledgeRetrievalResult:
        normalized_query = query.strip()
        if not normalized_query:
            return KnowledgeRetrievalResult(
                session_id=session_id,
                query=query,
                chunks=[],
                warnings=["Retrieval query is empty."],
            )

        if top_k <= 0:
            return KnowledgeRetrievalResult(
                session_id=session_id,
                query=normalized_query,
                chunks=[],
                warnings=["top_k must be greater than zero."],
            )

        embeddings = await self._embedding_provider.embed_texts([normalized_query])
        if not embeddings:
            return KnowledgeRetrievalResult(
                session_id=session_id,
                query=normalized_query,
                chunks=[],
                warnings=["Embedding provider returned no query embedding."],
            )

        retrieved_chunks = await self._vector_store.search(
            session_id=session_id,
            query_embedding=embeddings[0],
            top_k=top_k,
            document_types=document_types,
            filters=filters,
        )

        return KnowledgeRetrievalResult(
            session_id=session_id,
            query=normalized_query,
            chunks=[
                replace(chunk, retrieval_query=normalized_query)
                for chunk in retrieved_chunks
            ],
            warnings=[],
        )
