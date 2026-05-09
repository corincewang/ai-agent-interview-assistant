from pathlib import Path

from langchain_core.tools import StructuredTool

from app.domain.models import DocumentType
from app.tools.chunking import RecursiveTextChunkingTool
from app.tools.document_parsing import LocalDocumentParsingTool


def build_parse_document_tool(parser: LocalDocumentParsingTool) -> StructuredTool:
    async def parse_document(file_path: str, document_type: str) -> dict:
        parsed = await parser.parse_document(Path(file_path), DocumentType(document_type))
        return {
            "document_id": str(parsed.id),
            "document_type": parsed.document_type.value,
            "raw_text": parsed.raw_text,
            "metadata": parsed.metadata,
            "source_spans": [
                {
                    "document_id": str(span.document_id),
                    "page_number": span.page_number,
                    "start_char": span.start_char,
                    "end_char": span.end_char,
                    "text_excerpt": span.text_excerpt,
                }
                for span in parsed.source_spans
            ],
        }

    return StructuredTool.from_function(
        coroutine=parse_document,
        name="parse_document",
        description="Parse a PDF, Markdown, or text document into raw text with source spans.",
    )


def build_chunk_document_tool(chunker: RecursiveTextChunkingTool) -> StructuredTool:
    async def chunk_document(raw_text: str, document_type: str) -> list[dict]:
        from uuid import uuid4

        from app.domain.models import ParsedDocument

        document_id = uuid4()
        document = ParsedDocument(
            id=document_id,
            document_type=DocumentType(document_type),
            raw_text=raw_text,
            source_spans=[],
            metadata={},
        )
        chunks = await chunker.chunk_document(document)
        return [
            {
                "chunk_id": str(chunk.id),
                "document_id": str(chunk.document_id),
                "text": chunk.text,
                "metadata": chunk.metadata,
            }
            for chunk in chunks
        ]

    return StructuredTool.from_function(
        coroutine=chunk_document,
        name="chunk_document",
        description="Split parsed document text into overlapping retrieval chunks.",
    )

