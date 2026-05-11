from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import DocumentChunkRecord, DocumentRecord
from app.domain.models import (
    DocumentChunk,
    EmbeddedDocumentChunk,
    ParsedDocument,
)


class PostgresDocumentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_parsed_document(
        self,
        session_id: UUID,
        document: ParsedDocument,
        file_path: str | None = None,
    ) -> UUID:
        existing = await self.session.get(DocumentRecord, document.id)
        file_name = str(document.metadata.get("file_name") or document.id)

        if existing is None:
            record = DocumentRecord(
                id=document.id,
                session_id=session_id,
                document_type=document.document_type.value,
                file_name=file_name,
                file_path=file_path,
                raw_text=document.raw_text,
                document_metadata=document.metadata,
            )
            self.session.add(record)
        else:
            existing.document_type = document.document_type.value
            existing.file_name = file_name
            existing.file_path = file_path
            existing.raw_text = document.raw_text
            existing.document_metadata = document.metadata

        await self.session.flush()
        return document.id

    async def replace_chunks(
        self,
        session_id: UUID,
        document_id: UUID,
        chunks: list[DocumentChunk],
    ) -> list[UUID]:
        await self.session.execute(
            delete(DocumentChunkRecord).where(DocumentChunkRecord.document_id == document_id)
        )

        records = [_chunk_to_record(session_id, chunk) for chunk in chunks]
        self.session.add_all(records)
        await self.session.flush()
        return [record.id for record in records]

    async def upsert_embedded_chunks(
        self,
        session_id: UUID,
        chunks: list[EmbeddedDocumentChunk],
    ) -> list[UUID]:
        upserted_ids: list[UUID] = []

        for embedded_chunk in chunks:
            chunk = embedded_chunk.chunk
            record = await self.session.get(DocumentChunkRecord, chunk.id)
            if record is None:
                record = _chunk_to_record(session_id, chunk)
                self.session.add(record)

            record.document_type = str(chunk.metadata.get("document_type", "knowledge_base"))
            record.chunk_index = int(chunk.metadata.get("chunk_index", 0))
            record.text = chunk.text
            record.start_char = _optional_int(chunk.metadata.get("start_char"))
            record.end_char = _optional_int(chunk.metadata.get("end_char"))
            record.embedding_model = embedded_chunk.embedding_model
            record.embedding = embedded_chunk.embedding
            record.chunk_metadata = chunk.metadata
            upserted_ids.append(chunk.id)

        await self.session.flush()
        return upserted_ids

    async def list_chunks_for_document(self, document_id: UUID) -> list[DocumentChunk]:
        result = await self.session.scalars(
            select(DocumentChunkRecord)
            .where(DocumentChunkRecord.document_id == document_id)
            .order_by(DocumentChunkRecord.chunk_index)
        )
        return [_record_to_chunk(record) for record in result]


def _chunk_to_record(session_id: UUID, chunk: DocumentChunk) -> DocumentChunkRecord:
    return DocumentChunkRecord(
        id=chunk.id,
        session_id=session_id,
        document_id=chunk.document_id,
        document_type=str(chunk.metadata.get("document_type", "knowledge_base")),
        chunk_index=int(chunk.metadata.get("chunk_index", 0)),
        text=chunk.text,
        start_char=_optional_int(chunk.metadata.get("start_char")),
        end_char=_optional_int(chunk.metadata.get("end_char")),
        embedding_model=chunk.metadata.get("embedding_model"),
        embedding=None,
        chunk_metadata=chunk.metadata,
    )


def _record_to_chunk(record: DocumentChunkRecord) -> DocumentChunk:
    metadata = {
        **record.chunk_metadata,
        "document_type": record.document_type,
        "chunk_index": record.chunk_index,
        "start_char": record.start_char,
        "end_char": record.end_char,
        "embedding_model": record.embedding_model,
    }
    return DocumentChunk(
        id=record.id,
        document_id=record.document_id,
        text=record.text,
        metadata=metadata,
    )


def _optional_int(value: object) -> int | None:
    if value is None:
        return None
    return int(value)
