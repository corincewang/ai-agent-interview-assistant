from pathlib import Path
from typing import Any, Protocol
from uuid import UUID

from app.domain.models import (
    DocumentChunk,
    DocumentType,
    EmbeddedDocumentChunk,
    InterviewTurn,
    KnowledgeIndexingResult,
    KnowledgeRetrievalResult,
    ParsedDocument,
    RetrievedKnowledgeChunk,
    SourceCitation,
)


class DocumentParsingTool(Protocol):
    async def parse_document(
        self,
        file_path: Path,
        document_type: DocumentType,
        document_id: UUID | None = None,
    ) -> ParsedDocument:
        ...


class ChunkingTool(Protocol):
    async def chunk_document(self, document: ParsedDocument) -> list[DocumentChunk]:
        ...


class EmbeddingProvider(Protocol):
    async def embed_texts(self, texts: list[str]) -> list[list[float]]:
        ...


class VectorStore(Protocol):
    async def upsert_chunks(
        self,
        session_id: UUID,
        chunks: list[EmbeddedDocumentChunk],
    ) -> list[UUID]:
        ...

    async def search(
        self,
        session_id: UUID,
        query_embedding: list[float],
        top_k: int,
        document_types: list[DocumentType] | None = None,
        filters: dict[str, Any] | None = None,
    ) -> list[RetrievedKnowledgeChunk]:
        ...


class KnowledgeBaseIndexer(Protocol):
    async def index_documents(
        self,
        session_id: UUID,
        documents: list[ParsedDocument],
    ) -> KnowledgeIndexingResult:
        ...


class KnowledgeRetrievalTool(Protocol):
    async def retrieve_knowledge(
        self,
        session_id: UUID,
        query: str,
        top_k: int,
        document_types: list[DocumentType] | None = None,
        filters: dict[str, Any] | None = None,
    ) -> KnowledgeRetrievalResult:
        ...


class WebSearchTool(Protocol):
    async def search_web(self, query: str, limit: int) -> list[SourceCitation]:
        ...


class PageFetchTool(Protocol):
    async def fetch_public_page(self, url: str) -> str:
        ...


class SpeechToTextTool(Protocol):
    async def transcribe_audio(self, audio_path: Path) -> str:
        ...


class TextToSpeechTool(Protocol):
    async def synthesize_speech(self, text: str, voice: str) -> Path:
        ...


class InterviewPersistenceTool(Protocol):
    async def save_interview_turn(self, turn: InterviewTurn) -> UUID:
        ...

    async def load_interview_turns(self, session_id: UUID) -> list[InterviewTurn]:
        ...
