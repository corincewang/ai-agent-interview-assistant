from pydantic import BaseModel, Field

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool, tool
from langgraph.prebuilt import create_react_agent

from app.domain.models import DocumentType, ResearchFinding, SourceCitation
from app.ports.tools import PageFetchTool, WebSearchTool


class SourceCitationResponse(BaseModel):
    title: str
    url: str | None = None
    source_type: str = "interview_intel"
    confidence: float = Field(default=0.5, ge=0.0, le=1.0)


class ResearchFindingResponse(BaseModel):
    citation: SourceCitationResponse
    summary: str
    relevant_topics: list[str] = Field(default_factory=list)
    extracted_signals: list[str] = Field(default_factory=list)


class InterviewIntelResponse(BaseModel):
    findings: list[ResearchFindingResponse] = Field(default_factory=list)


class LLMInterviewIntelSkill:
    def __init__(
        self,
        llm: BaseChatModel,
        web_search_tool: WebSearchTool,
        page_fetch_tool: PageFetchTool | None = None,
        search_limit: int = 5,
    ) -> None:
        self.llm = llm
        self.web_search_tool = web_search_tool
        self.page_fetch_tool = page_fetch_tool
        self.search_limit = search_limit

    async def collect_interview_intel(
        self,
        company_name: str,
        role_title: str,
        topics: list[str],
    ) -> list[ResearchFinding]:
        agent = create_react_agent(
            model=self.llm,
            tools=self._build_react_tools(),
            prompt=(
                "You collect public interview preparation signals for software engineering roles. "
                "Use tools to search and fetch source text when useful. "
                "Extract only reusable interview topics, question patterns, and role-relevant signals. "
                "Do not claim that a company will ask a question unless source text supports it. "
                "Return concise structured findings with citation metadata."
            ),
            response_format=InterviewIntelResponse,
            name="interview_intel_react_agent",
        )
        response = await agent.ainvoke(
            {
                "messages": [
                    HumanMessage(
                        content=(
                            f"Company: {company_name}\n"
                            f"Role: {role_title}\n"
                            f"Target topics: {topics}\n"
                            f"Suggested query: {self._build_query(company_name, role_title, topics)}"
                        )
                    )
                ]
            }
        )
        structured_response = response.get("structured_response")
        if structured_response is None:
            return []

        return [
            self._to_research_finding(finding)
            for finding in structured_response.findings[: self.search_limit]
        ]

    def _build_query(self, company_name: str, role_title: str, topics: list[str]) -> str:
        topic_terms = " ".join(topics[:6])
        return f"{company_name} {role_title} software engineer interview questions {topic_terms}".strip()

    def _build_react_tools(self) -> list[BaseTool]:
        @tool
        async def search_interview_sources(query: str, limit: int = 5) -> list[dict]:
            """Search public sources for company or role interview preparation signals."""
            citations = await self.web_search_tool.search_web(
                query=query,
                limit=min(limit, self.search_limit),
            )
            return [
                {
                    "title": citation.title,
                    "url": citation.url,
                    "source_type": citation.source_type.value,
                    "confidence": citation.confidence,
                }
                for citation in citations
            ]

        @tool
        async def fetch_source_text(url: str) -> str:
            """Fetch readable page text for a public citation URL."""
            if self.page_fetch_tool is None:
                return ""
            try:
                return await self.page_fetch_tool.fetch_public_page(url)
            except Exception:
                return ""

        return [search_interview_sources, fetch_source_text]

    def _to_research_finding(self, finding: ResearchFindingResponse) -> ResearchFinding:
        citation = SourceCitation(
            title=finding.citation.title,
            url=finding.citation.url,
            source_type=_coerce_document_type(finding.citation.source_type),
            confidence=finding.citation.confidence,
        )
        return ResearchFinding(
            citation=citation,
            summary=finding.summary,
            relevant_topics=finding.relevant_topics,
            extracted_signals=finding.extracted_signals,
        )


def _coerce_document_type(value: str) -> DocumentType:
    try:
        return DocumentType(value)
    except ValueError:
        return DocumentType.INTERVIEW_INTEL
