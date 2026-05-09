from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.domain.models import JobAnalysis, ResearchFinding, SourceCitation
from app.ports.tools import PageFetchTool, WebSearchTool


class LLMCompanyResearchSkill:
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
                    "You summarize public company and role research for technical interview preparation. "
                    "Extract only role-relevant engineering, product, team, or interview preparation signals. "
                    "Do not invent facts that are not supported by the source text.",
                ),
                (
                    "human",
                    "Company: {company_name}\n"
                    "Role: {role_title}\n"
                    "Job analysis: {jd_analysis}\n\n"
                    "Source citation: {citation}\n\n"
                    "Source text:\n{source_text}",
                ),
            ]
        )

    async def research_company_and_role(
        self,
        company_name: str,
        role_title: str,
        jd_analysis: JobAnalysis,
    ) -> list[ResearchFinding]:
        citations = await self.web_search_tool.search_web(
            query=self._build_query(company_name, role_title, jd_analysis),
            limit=self.search_limit,
        )

        findings: list[ResearchFinding] = []
        for citation in citations:
            source_text = await self._fetch_source_text(citation)
            findings.append(
                await self._summarize_source(
                    company_name=company_name,
                    role_title=role_title,
                    jd_analysis=jd_analysis,
                    citation=citation,
                    source_text=source_text,
                )
            )

        return findings

    def _build_query(
        self,
        company_name: str,
        role_title: str,
        jd_analysis: JobAnalysis,
    ) -> str:
        skill_terms = " ".join(jd_analysis.required_skills[:5])
        return f"{company_name} {role_title} engineering interview role {skill_terms}".strip()

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
        jd_analysis: JobAnalysis,
        citation: SourceCitation,
        source_text: str,
    ) -> ResearchFinding:
        if not source_text.strip():
            return ResearchFinding(
                citation=citation,
                summary="Source discovered, but page text was unavailable for summarization.",
                relevant_topics=[],
                extracted_signals=[],
            )

        structured_llm = self.llm.with_structured_output(ResearchFinding)
        chain = self.prompt | structured_llm
        return await chain.ainvoke(
            {
                "company_name": company_name,
                "role_title": role_title,
                "jd_analysis": jd_analysis,
                "citation": citation,
                "source_text": source_text[:8000],
            }
        )

