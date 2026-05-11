from dataclasses import replace
from uuid import UUID

from app.domain.models import (
    EmbeddedDocumentChunk,
    KnowledgeIndexingResult,
    ParsedDocument,
)
from app.ports.tools import ChunkingTool, EmbeddingProvider, VectorStore


class DefaultKnowledgeBaseIndexer:
    def __init__(
        self,
        chunking_tool: ChunkingTool,
        embedding_provider: EmbeddingProvider,
        vector_store: VectorStore,
    ) -> None:
        self._chunking_tool = chunking_tool
        self._embedding_provider = embedding_provider
        self._vector_store = vector_store

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
            chunks = await self._chunking_tool.chunk_document(document)
            if not chunks:
                skipped_document_ids.append(document.id)
                warnings.append(f"Document {document.id} produced no chunks.")
                continue

            texts = [chunk.text for chunk in chunks]
            embeddings = await self._embedding_provider.embed_texts(texts)
            if len(embeddings) != len(chunks):
                skipped_document_ids.append(document.id)
                warnings.append(
                    f"Document {document.id} produced {len(chunks)} chunks but "
                    f"{len(embeddings)} embeddings."
                )
                continue

            embedding_model = getattr(self._embedding_provider, "model", "unknown")
            embedded_chunks = [
                EmbeddedDocumentChunk(
                    chunk=replace(
                        chunk,
                        metadata={
                            **chunk.metadata,
                            "session_id": str(session_id),
                            "embedding_model": embedding_model,
                        },
                    ),
                    embedding=embedding,
                    embedding_model=embedding_model,
                )
                for chunk, embedding in zip(chunks, embeddings)
            ]

            upserted_chunk_ids = await self._vector_store.upsert_chunks(
                session_id=session_id,
                chunks=embedded_chunks,
            )
            indexed_document_ids.append(document.id)
            indexed_chunk_ids.extend(upserted_chunk_ids)

        return KnowledgeIndexingResult(
            session_id=session_id,
            indexed_document_ids=indexed_document_ids,
            indexed_chunk_ids=indexed_chunk_ids,
            skipped_document_ids=skipped_document_ids,
            warnings=warnings,
        )
