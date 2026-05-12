"""Index knowledge-base PDFs in page-window batches using `parse_document_windows` + embed + upsert."""

from pathlib import Path
from uuid import UUID

from app.domain.models import (
    DocumentType,
    KnowledgeIndexingResult,
    ParsedDocument,
)
from app.ports.tools import ChunkingTool, EmbeddingProvider, VectorStore
from app.tools.document_parsing import LocalDocumentParsingTool
from app.tools.streaming_ingestion import StreamingKnowledgeBaseIngestion


class WindowedKnowledgeBaseIndexer:
    """Chunk and embed PDFs roughly 10 pages at a time (see `PDF_PAGE_WINDOW_SIZE`)."""

    def __init__(
        self,
        document_parser: LocalDocumentParsingTool,
        chunking_tool: ChunkingTool,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ) -> None:
        self._streaming = StreamingKnowledgeBaseIngestion(
            document_parsing_tool=document_parser,
            chunking_tool=chunking_tool,
            embedding_provider=embedding_provider,
            vector_store=vector_store,
        )

    async def index_documents(
        self,
        session_id: UUID,
        documents: list[ParsedDocument],
    ) -> KnowledgeIndexingResult:
        indexed_document_ids: list[UUID] = []
        indexed_chunk_ids: list[UUID] = []
        skipped_document_ids: list[UUID] = []
        warnings: list[str] = []

        for document in documents:
            if document.document_type != DocumentType.KNOWLEDGE_BASE:
                continue

            path_str = document.metadata.get("source_file_path")
            if not isinstance(path_str, str) or not path_str.strip():
                skipped_document_ids.append(document.id)
                warnings.append(
                    f"Skipped knowledge document {document.id}: missing metadata source_file_path."
                )
                continue

            resolved_path = Path(path_str)
            if not resolved_path.is_file():
                skipped_document_ids.append(document.id)
                warnings.append(
                    f"Skipped knowledge document {document.id}: path not found: {resolved_path}."
                )
                continue

            last_chunk_ids: list[UUID] = []
            collected_warnings: list[str] = []

            async for progress in self._streaming.ingest_document(
                session_id=session_id,
                file_path=resolved_path,
                document_type=DocumentType.KNOWLEDGE_BASE,
                document_id=document.id,
            ):
                collected_warnings.extend(progress.warnings)
                if progress.status == "completed":
                    last_chunk_ids = progress.indexed_chunk_ids

            warnings.extend(collected_warnings)

            if last_chunk_ids:
                indexed_document_ids.append(document.id)
                indexed_chunk_ids.extend(last_chunk_ids)
            else:
                skipped_document_ids.append(document.id)
                warnings.append(
                    f"No chunks indexed for knowledge document {document.id} ({resolved_path.name})."
                )

        return KnowledgeIndexingResult(
            session_id=session_id,
            indexed_document_ids=indexed_document_ids,
            indexed_chunk_ids=indexed_chunk_ids,
            skipped_document_ids=skipped_document_ids,
            warnings=warnings,
        )
