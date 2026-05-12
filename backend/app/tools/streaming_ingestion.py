from collections.abc import AsyncIterator
from dataclasses import replace
from pathlib import Path
from uuid import UUID, uuid4

from app.domain.models import (
    DocumentType,
    EmbeddedDocumentChunk,
    KnowledgeIngestionProgress,
    ParsedDocument,
)
from app.ports.tools import ChunkingTool, EmbeddingProvider, VectorStore
from app.tools.document_parsing import LocalDocumentParsingTool


class StreamingKnowledgeBaseIngestion:
    def __init__(
        self,
        document_parsing_tool: LocalDocumentParsingTool,
        chunking_tool: ChunkingTool,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ) -> None:
        self._document_parsing_tool = document_parsing_tool
        self._chunking_tool = chunking_tool
        self._embedding_provider = embedding_provider
        self._vector_store = vector_store

    async def ingest_document(
        self,
        session_id: UUID,
        file_path: Path,
        document_type: DocumentType,
        document_id: UUID | None = None,
    ) -> AsyncIterator[KnowledgeIngestionProgress]:
        resolved_document_id = document_id or uuid4()
        total_indexed_chunk_count = 0
        total_indexed_chunk_ids = []
        warnings: list[str] = []

        async for parsed_window in self._document_parsing_tool.parse_document_windows(
            file_path=file_path,
            document_type=document_type,
            document_id=resolved_document_id,
        ):
            progress = await self._index_parsed_window(
                session_id=session_id,
                parsed_window=parsed_window,
            )
            warnings.extend(progress.warnings)
            total_indexed_chunk_count += progress.indexed_chunk_count
            total_indexed_chunk_ids.extend(progress.indexed_chunk_ids)
            yield progress

        yield KnowledgeIngestionProgress(
            session_id=session_id,
            document_id=resolved_document_id,
            status="completed",
            page_window=None,
            parsed_char_count=0,
            chunk_count=0,
            indexed_chunk_count=total_indexed_chunk_count,
            indexed_chunk_ids=total_indexed_chunk_ids,
            warnings=warnings,
        )

    async def _index_parsed_window(
        self,
        session_id: UUID,
        parsed_window: ParsedDocument,
    ) -> KnowledgeIngestionProgress:
        chunks = await self._chunking_tool.chunk_document(parsed_window)
        page_window = _page_window(parsed_window)

        if not chunks:
            return KnowledgeIngestionProgress(
                session_id=session_id,
                document_id=parsed_window.id,
                status="skipped_window",
                page_window=page_window,
                parsed_char_count=len(parsed_window.raw_text),
                chunk_count=0,
                indexed_chunk_count=0,
                indexed_chunk_ids=[],
                warnings=[f"Window {page_window} produced no chunks."],
            )

        embedding_model = getattr(self._embedding_provider, "model", "unknown")
        embeddings = await self._embedding_provider.embed_texts([chunk.text for chunk in chunks])
        if len(embeddings) != len(chunks):
            return KnowledgeIngestionProgress(
                session_id=session_id,
                document_id=parsed_window.id,
                status="skipped_window",
                page_window=page_window,
                parsed_char_count=len(parsed_window.raw_text),
                chunk_count=len(chunks),
                indexed_chunk_count=0,
                indexed_chunk_ids=[],
                warnings=[
                    f"Window {page_window} produced {len(chunks)} chunks but "
                    f"{len(embeddings)} embeddings."
                ],
            )

        embedded_chunks = [
            EmbeddedDocumentChunk(
                chunk=replace(
                    chunk,
                    metadata={
                        **chunk.metadata,
                        "session_id": str(session_id),
                        "embedding_model": embedding_model,
                        "source_file_name": parsed_window.metadata.get("file_name"),
                        "page_window": page_window,
                        "parser_strategy": parsed_window.metadata.get("parser_strategy"),
                    },
                ),
                embedding=embedding,
                embedding_model=embedding_model,
            )
            for chunk, embedding in zip(chunks, embeddings)
        ]
        indexed_chunk_ids = await self._vector_store.upsert_chunks(
            session_id=session_id,
            chunks=embedded_chunks,
        )

        return KnowledgeIngestionProgress(
            session_id=session_id,
            document_id=parsed_window.id,
            status="indexed_window",
            page_window=page_window,
            parsed_char_count=len(parsed_window.raw_text),
            chunk_count=len(chunks),
            indexed_chunk_count=len(indexed_chunk_ids),
            indexed_chunk_ids=indexed_chunk_ids,
            warnings=[],
        )


def _page_window(parsed_document: ParsedDocument) -> dict[str, int] | None:
    page_window = parsed_document.metadata.get("page_window")
    if not isinstance(page_window, dict):
        return None

    start_page = page_window.get("start_page")
    end_page = page_window.get("end_page")
    if not isinstance(start_page, int) or not isinstance(end_page, int):
        return None

    return {"start_page": start_page, "end_page": end_page}
