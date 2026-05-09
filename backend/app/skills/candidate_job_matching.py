from uuid import UUID

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.domain.models import CandidateJobMatch, CandidateProfile, JobAnalysis


class LLMCandidateJobMatchingSkill:
    def __init__(self, llm: BaseChatModel) -> None:
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You compare a candidate profile against a software engineering job analysis. "
                    "Identify concrete matches, gaps, role-specific risks, and recommended interview positioning. "
                    "Base every judgment on the provided candidate profile and job analysis.",
                ),
                (
                    "human",
                    "Session ID: {session_id}\n\n"
                    "Candidate profile:\n{candidate_profile}\n\n"
                    "Job analysis:\n{job_analysis}",
                ),
            ]
        )

    async def match_candidate_to_job(
        self,
        session_id: UUID,
        candidate_profile: CandidateProfile,
        job_analysis: JobAnalysis,
    ) -> CandidateJobMatch:
        structured_llm = self.llm.with_structured_output(CandidateJobMatch)
        chain = self.prompt | structured_llm
        return await chain.ainvoke(
            {
                "session_id": str(session_id),
                "candidate_profile": candidate_profile,
                "job_analysis": job_analysis,
            }
        )

