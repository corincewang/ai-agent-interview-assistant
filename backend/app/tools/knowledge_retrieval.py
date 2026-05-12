from dataclasses import replace
from typing import Any
from uuid import UUID

from app.domain.models import (
    DocumentType,
    KnowledgeRetrievalResult,
)
from app.ports.tools import EmbeddingProvider, VectorStore
from app.tools.knowledge_reranker import rerank_retrieved_chunks


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
        prefetch_k: int | None = None,
        rerank_enabled: bool = True,
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

        fetch_cap = prefetch_k if prefetch_k is not None else max(20, top_k)
        fetch_cap = max(fetch_cap, top_k)

        retrieved_chunks = await self._vector_store.search(
            session_id=session_id,
            query_embedding=embeddings[0],
            top_k=fetch_cap,
            document_types=document_types,
            filters=filters,
        )

        if rerank_enabled and len(retrieved_chunks) > 1:
            retrieved_chunks = rerank_retrieved_chunks(normalized_query, retrieved_chunks)

        retrieved_chunks = retrieved_chunks[:top_k]
        retrieved_chunks = [
            replace(chunk, rank=ordinal)
            for ordinal, chunk in enumerate(retrieved_chunks, start=1)
        ]

        return KnowledgeRetrievalResult(
            session_id=session_id,
            query=normalized_query,
            chunks=[
                replace(chunk, retrieval_query=normalized_query)
                for chunk in retrieved_chunks
            ],
            warnings=[],
        )
