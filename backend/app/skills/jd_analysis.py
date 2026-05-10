from uuid import UUID

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.domain.models import JobAnalysis
from app.utils.dataclass_mapping import coerce_dataclass


class LLMJDAnalysisSkill:
    def __init__(self, llm: BaseChatModel) -> None:
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You analyze software engineering job descriptions for interview preparation. "
                    "Extract concrete requirements, preferred qualifications, responsibilities, "
                    "candidate matches, and candidate gaps. Do not invent company-specific details "
                    "that are not present in the JD.",
                ),
                (
                    "human",
                    "Session ID: {session_id}\n"
                    "Company: {company_name}\n"
                    "Role: {role_title}\n\n"
                    "Job description:\n{jd_text}",
                ),
            ]
        )

    async def analyze_job_description(
        self,
        session_id: UUID,
        company_name: str,
        role_title: str,
        jd_text: str,
    ) -> JobAnalysis:
        structured_llm = self.llm.with_structured_output(JobAnalysis)
        chain = self.prompt | structured_llm
        extracted = await chain.ainvoke(
            {
                "session_id": str(session_id),
                "company_name": company_name,
                "role_title": role_title,
                "jd_text": jd_text,
            }
        )
        return coerce_dataclass(JobAnalysis, extracted)
