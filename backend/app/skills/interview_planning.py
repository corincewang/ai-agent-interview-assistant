from uuid import UUID

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import ChatPromptTemplate

from app.domain.models import (
    CandidateJobMatch,
    CandidateProfile,
    InterviewPlan,
    JobAnalysis,
    ResearchFinding,
)


class LLMInterviewPlanningSkill:
    def __init__(self, llm: BaseChatModel) -> None:
        self.llm = llm
        self.prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You create structured technical interview plans. "
                    "Use the candidate profile, job analysis, candidate-job match, company context, "
                    "and interview intel to generate focused questions and follow-up strategies. "
                    "Every question should test a concrete signal, risk area, or role requirement.",
                ),
                (
                    "human",
                    "Session ID: {session_id}\n\n"
                    "Candidate profile:\n{candidate_profile}\n\n"
                    "Job analysis:\n{job_analysis}\n\n"
                    "Candidate-job match:\n{candidate_job_match}\n\n"
                    "Company sources:\n{company_sources}\n\n"
                    "Interview intel:\n{interview_intel}",
                ),
            ]
        )

    async def create_interview_plan(
        self,
        session_id: UUID,
        candidate_profile: CandidateProfile,
        job_analysis: JobAnalysis,
        candidate_job_match: CandidateJobMatch,
        company_sources: list[ResearchFinding],
        interview_intel: list[ResearchFinding],
    ) -> InterviewPlan:
        structured_llm = self.llm.with_structured_output(InterviewPlan)
        chain = self.prompt | structured_llm
        return await chain.ainvoke(
            {
                "session_id": str(session_id),
                "candidate_profile": candidate_profile,
                "job_analysis": job_analysis,
                "candidate_job_match": candidate_job_match,
                "company_sources": company_sources,
                "interview_intel": interview_intel,
            }
        )
