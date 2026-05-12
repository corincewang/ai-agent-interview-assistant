import re
from uuid import uuid4

from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter

from app.domain.models import DocumentChunk, ParsedDocument


class RecursiveTextChunkingTool:
    def __init__(self, chunk_size: int = 900, chunk_overlap: int = 120) -> None:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be positive")
        if chunk_overlap < 0:
            raise ValueError("chunk_overlap cannot be negative")
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be smaller than chunk_size")

        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self._markdown_splitter = MarkdownHeaderTextSplitter(
            headers_to_split_on=[
                ("#", "h1"),
                ("##", "h2"),
                ("###", "h3"),
            ],
            strip_headers=True,
        )
        self._recursive_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", "。", ".", " ", ""],
        )

    async def chunk_document(self, document: ParsedDocument) -> list[DocumentChunk]:
        text = document.raw_text.strip()
        if not text:
            return []

        markdown_text = _to_section_markdown(document)
        markdown_documents = self._markdown_splitter.split_text(markdown_text)
        section_spans = _section_spans_by_title(document)
        chunks: list[DocumentChunk] = []

        for markdown_document in markdown_documents:
            structured_text = _format_chunk_text(
                content=markdown_document.page_content,
                metadata=markdown_document.metadata,
            )
            if not structured_text:
                continue

            split_texts = (
                [structured_text]
                if len(structured_text) <= self.chunk_size
                else self._recursive_splitter.split_text(structured_text)
            )

            for split_text in split_texts:
                chunk_text = split_text.strip()
                if not chunk_text:
                    continue

                section_title = _section_title(markdown_document.metadata)
                section_span = section_spans.get(section_title or "")
                chunks.append(
                    DocumentChunk(
                        id=uuid4(),
                        document_id=document.id,
                        text=chunk_text,
                        metadata={
                            "document_type": document.document_type.value,
                            "start_char": section_span[0] if section_span else None,
                            "end_char": section_span[1] if section_span else None,
                            "chunk_index": len(chunks),
                            "chunk_strategy": "markdown_header_structure",
                            "section_path": _section_path(markdown_document.metadata),
                            "section_title": section_title,
                            "source_file_name": document.metadata.get("file_name"),
                            "page_window": document.metadata.get("page_window"),
                        },
                    )
                )

        return chunks


def _to_section_markdown(document: ParsedDocument) -> str:
    sections = _normalized_sections(document)
    if not sections:
        return document.raw_text

    markdown_parts: list[str] = []
    for section in sections:
        title = str(section["title"]).strip()
        level = _markdown_level(section.get("level"))
        start_char = int(section["start_char"])
        end_char = int(section["end_char"])
        body = document.raw_text[start_char:end_char].strip()
        body = _remove_repeated_heading(body, title)
        if not body:
            continue

        markdown_parts.append(f"{'#' * level} {title}\n\n{body}")

    return "\n\n".join(markdown_parts) if markdown_parts else document.raw_text


def _section_spans_by_title(document: ParsedDocument) -> dict[str, tuple[int, int]]:
    return {
        str(section["title"]): (
            int(section["start_char"]),
            int(section["end_char"]),
        )
        for section in _normalized_sections(document)
    }


def _normalized_sections(document: ParsedDocument) -> list[dict[str, object]]:
    raw_sections = document.metadata.get("sections")
    if not isinstance(raw_sections, list):
        return []

    heading_candidates: list[dict[str, object]] = []
    text_length = len(document.raw_text)
    for section in raw_sections:
        if not isinstance(section, dict):
            continue

        title = section.get("title")
        start_char = section.get("start_char")
        end_char = section.get("end_char")
        if not isinstance(title, str):
            continue
        if not isinstance(start_char, int) or not isinstance(end_char, int):
            continue
        if start_char < 0 or end_char <= start_char or start_char >= text_length:
            continue

        normalized_title = _normalize_section_title(title)
        if not _looks_like_structural_heading(normalized_title):
            continue

        heading_candidates.append(
            {
                **section,
                "title": normalized_title,
                "start_char": start_char,
                "end_char": min(end_char, text_length),
            }
        )

    heading_candidates.sort(key=lambda item: int(item["start_char"]))

    sections: list[dict[str, object]] = []
    for index, heading in enumerate(heading_candidates):
        next_start = (
            int(heading_candidates[index + 1]["start_char"])
            if index + 1 < len(heading_candidates)
            else text_length
        )
        if next_start <= int(heading["start_char"]):
            continue

        sections.append(
            {
                **heading,
                "end_char": next_start,
            }
        )

    return sections


def _normalize_section_title(title: str) -> str:
    title = " ".join(title.strip().split())
    for marker in ("？", "?"):
        if marker in title:
            return title.split(marker, 1)[0].strip() + marker
    return title[:80]


def _looks_like_structural_heading(title: str) -> bool:
    if not title:
        return False
    if len(title) <= 36 and not title.endswith(("。", "，", ",", "；", ";")):
        return True
    if "?" in title or "？" in title:
        return True
    if re.match(r"^(Q\d+|Q\d+\.\d+|追问\s*\d*|第[一二三四五六七八九十\d]+[章节部分])", title):
        return True
    if re.match(r"^(为什么|怎么|如何|什么是|介绍一下|讲一下|说一下|谈谈)", title):
        return True
    return False


def _markdown_level(value: object) -> int:
    if not isinstance(value, int):
        return 2
    return min(max(value, 1), 3)


def _remove_repeated_heading(body: str, title: str) -> str:
    if body.startswith(title):
        return body[len(title) :].strip()
    return body


def _format_chunk_text(content: str, metadata: dict[str, str]) -> str:
    content = content.strip()
    section_path = _section_path(metadata)
    if not section_path:
        return content

    return f"{section_path}\n\n{content}".strip()


def _section_path(metadata: dict[str, str]) -> str | None:
    titles = [
        metadata[key].strip()
        for key in ("h1", "h2", "h3")
        if metadata.get(key, "").strip()
    ]
    return " > ".join(titles) if titles else None


def _section_title(metadata: dict[str, str]) -> str | None:
    for key in ("h3", "h2", "h1"):
        value = metadata.get(key, "").strip()
        if value:
            return value
    return None
