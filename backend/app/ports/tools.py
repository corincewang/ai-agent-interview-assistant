from pathlib import Path
from typing import Protocol
from uuid import UUID

from app.domain.models import DocumentChunk, DocumentType, InterviewTurn, ParsedDocument, SourceCitation


class DocumentParsingTool(Protocol):
    async def parse_document(self, file_path: Path, document_type: DocumentType) -> ParsedDocument:
        ...


class ChunkingTool(Protocol):
    async def chunk_document(self, document: ParsedDocument) -> list[DocumentChunk]:
        ...


class EmbeddingTool(Protocol):
    async def embed_chunks(self, chunks: list[DocumentChunk]) -> list[UUID]:
        ...


class RetrievalTool(Protocol):
    async def retrieve_context(
        self,
        session_id: UUID,
        query: str,
        document_types: list[DocumentType],
        limit: int,
    ) -> list[DocumentChunk]:
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
