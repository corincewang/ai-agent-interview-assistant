from app.domain.models import DocumentType, SourceCitation


class MockWebSearchTool:
    async def search_web(self, query: str, limit: int) -> list[SourceCitation]:
        citations = [
            SourceCitation(
                title="Mock company engineering overview",
                url="mock://company-engineering-overview",
                source_type=DocumentType.COMPANY_RESEARCH,
                confidence=0.7,
            ),
            SourceCitation(
                title="Mock software engineering interview patterns",
                url="mock://interview-patterns",
                source_type=DocumentType.INTERVIEW_INTEL,
                confidence=0.65,
            ),
        ]
        return citations[:limit]


class MockPageFetchTool:
    async def fetch_public_page(self, url: str) -> str:
        pages = {
            "mock://company-engineering-overview": (
                "The company values product-minded engineers who can work across frontend, backend, "
                "and AI-assisted workflows. Engineering interviews often emphasize practical system "
                "design, ownership, testing, and clear communication about tradeoffs."
            ),
            "mock://interview-patterns": (
                "Common technical interview signals include project deep dives, debugging approach, "
                "API design, frontend state management, data modeling, and the ability to explain "
                "AI agent tool-calling architecture with failure handling."
            ),
        }
        return pages.get(url, "")

