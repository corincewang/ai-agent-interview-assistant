from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import DocumentChunkRecord
from app.domain.models import (
    DocumentChunk,
    DocumentType,
    EmbeddedDocumentChunk,
    RetrievedKnowledgeChunk,
)
from app.repositories.documents import PostgresDocumentRepository


class PostgresVectorStore:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.document_repository = PostgresDocumentRepository(session)

    async def upsert_chunks(
        self,
        session_id: UUID,
        chunks: list[EmbeddedDocumentChunk],
    ) -> list[UUID]:
        return await self.document_repository.upsert_embedded_chunks(
            session_id=session_id,
            chunks=chunks,
        )

    async def search(
        self,
        session_id: UUID,
        query_embedding: list[float],
        top_k: int,
        document_types: list[DocumentType] | None = None,
        filters: dict[str, Any] | None = None,
    ) -> list[RetrievedKnowledgeChunk]:
        if top_k <= 0:
            return []

        distance = DocumentChunkRecord.embedding.cosine_distance(query_embedding).label(
            "distance"
        )
        statement = (
            select(DocumentChunkRecord, distance)
            .where(DocumentChunkRecord.session_id == session_id)
            .where(DocumentChunkRecord.embedding.is_not(None))
            .order_by(distance)
            .limit(top_k)
        )

        if document_types:
            statement = statement.where(
                DocumentChunkRecord.document_type.in_(
                    [document_type.value for document_type in document_types]
                )
            )

        if filters:
            for key, value in filters.items():
                statement = statement.where(
                    DocumentChunkRecord.chunk_metadata[key].astext == str(value)
                )

        rows = (await self.session.execute(statement)).all()
        return [
            RetrievedKnowledgeChunk(
                chunk=_record_to_chunk(record),
                score=1.0 - float(distance_value),
                rank=index,
                retrieval_query="<embedding>",
            )
            for index, (record, distance_value) in enumerate(rows, start=1)
        ]


def _record_to_chunk(record: DocumentChunkRecord) -> DocumentChunk:
    return DocumentChunk(
        id=record.id,
        document_id=record.document_id,
        text=record.text,
        metadata={
            **record.chunk_metadata,
            "document_type": record.document_type,
            "chunk_index": record.chunk_index,
            "start_char": record.start_char,
            "end_char": record.end_char,
            "embedding_model": record.embedding_model,
        },
    )
