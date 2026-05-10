from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.domain.models import ResearchFinding, SourceCitation
from app.ports.tools import PageFetchTool, WebSearchTool
from app.utils.dataclass_mapping import coerce_dataclass


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
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You summarize public interview preparation signals for software engineering roles. "
                    "Extract only reusable interview topics, question patterns, and role-relevant signals. "
                    "Do not claim that a company will ask a question unless the source explicitly supports it.",
                ),
                (
                    "human",
                    "Company: {company_name}\n"
                    "Role: {role_title}\n"
                    "Target topics: {topics}\n\n"
                    "Source citation: {citation}\n\n"
                    "Source text:\n{source_text}",
                ),
            ]
        )

    async def collect_interview_intel(
        self,
        company_name: str,
        role_title: str,
        topics: list[str],
    ) -> list[ResearchFinding]:
        citations = await self.web_search_tool.search_web(
            query=self._build_query(company_name, role_title, topics),
            limit=self.search_limit,
        )

        findings: list[ResearchFinding] = []
        for citation in citations:
            source_text = await self._fetch_source_text(citation)
            findings.append(
                await self._summarize_source(
                    company_name=company_name,
                    role_title=role_title,
                    topics=topics,
                    citation=citation,
                    source_text=source_text,
                )
            )

        return findings

    def _build_query(self, company_name: str, role_title: str, topics: list[str]) -> str:
        topic_terms = " ".join(topics[:6])
        return f"{company_name} {role_title} software engineer interview questions {topic_terms}".strip()

    async def _fetch_source_text(self, citation: SourceCitation) -> str:
        if self.page_fetch_tool is None or citation.url is None:
            return ""

        try:
            return await self.page_fetch_tool.fetch_public_page(citation.url)
        except Exception:
            return ""

    async def _summarize_source(
        self,
        company_name: str,
        role_title: str,
        topics: list[str],
        citation: SourceCitation,
        source_text: str,
    ) -> ResearchFinding:
        if not source_text.strip():
            return ResearchFinding(
                citation=citation,
                summary="Source discovered, but page text was unavailable for interview-intel summarization.",
                relevant_topics=[],
                extracted_signals=[],
            )

        structured_llm = self.llm.with_structured_output(ResearchFinding)
        chain = self.prompt | structured_llm
        extracted = await chain.ainvoke(
            {
                "company_name": company_name,
                "role_title": role_title,
                "topics": topics,
                "citation": citation,
                "source_text": source_text[:8000],
            }
        )
        return coerce_dataclass(ResearchFinding, extracted)
