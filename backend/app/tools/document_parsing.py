import re
from pathlib import Path
from uuid import UUID, uuid4

from pypdf import PdfReader

from app.domain.models import DocumentType, ParsedDocument, SourceSpan


class LocalDocumentParsingTool:
    async def parse_document(
        self,
        file_path: Path,
        document_type: DocumentType,
        document_id: UUID | None = None,
    ) -> ParsedDocument:
        suffix = file_path.suffix.lower()

        if suffix == ".pdf":
            return self._parse_pdf(file_path, document_type, document_id)

        if suffix in {".txt", ".md"}:
            return self._parse_text(file_path, document_type, document_id)

        raise ValueError(f"Unsupported document type: {suffix}")

    def _parse_pdf(
        self,
        file_path: Path,
        document_type: DocumentType,
        document_id: UUID | None,
    ) -> ParsedDocument:
        document_id = document_id or uuid4()
        suffix = file_path.suffix.lower()
        reader = PdfReader(str(file_path))
        page_texts: list[str] = []
        source_spans: list[SourceSpan] = []
        cursor = 0

        for page_index, page in enumerate(reader.pages, start=1):
            text = _clean_extracted_text(page.extract_text() or "")
            if not text.strip():
                continue

            start = cursor
            page_texts.append(text)
            cursor += len(text)

            source_spans.append(
                SourceSpan(
                    document_id=document_id,
                    page_number=page_index,
                    start_char=start,
                    end_char=cursor,
                    text_excerpt=text[:500],
                )
            )
            cursor += 1

        return ParsedDocument(
            id=document_id,
            document_type=document_type,
            raw_text="\n".join(page_texts),
            source_spans=source_spans,
            metadata={
                "file_name": file_path.name,
                "file_suffix": suffix,
                "page_count": len(reader.pages),
            },
        )

    def _parse_text(
        self,
        file_path: Path,
        document_type: DocumentType,
        document_id: UUID | None,
    ) -> ParsedDocument:
        document_id = document_id or uuid4()
        text = _clean_extracted_text(file_path.read_text(encoding="utf-8"))

        return ParsedDocument(
            id=document_id,
            document_type=document_type,
            raw_text=text,
            source_spans=[
                SourceSpan(
                    document_id=document_id,
                    page_number=None,
                    start_char=0,
                    end_char=len(text),
                    text_excerpt=text[:500],
                )
            ],
            metadata={
                "file_name": file_path.name,
                "file_suffix": file_path.suffix.lower(),
            },
        )


def _clean_extracted_text(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])", "", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff])\s+(?=[，。！？；：（）、])", "", text)
    text = re.sub(r"(?<=[，。！？；：（）、])\s+(?=[\u4e00-\u9fff])", "", text)
    text = re.sub(r"(?<=[A-Za-z0-9])\s*\n+\s*(?=[A-Za-z0-9])", " ", text)
    text = re.sub(r"(?<=[A-Za-z0-9])\s*\n+\s*(?=[\u4e00-\u9fff])", " ", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff])\s*\n+\s*(?=[A-Za-z0-9])", " ", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()
