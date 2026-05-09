from typing import Protocol
from uuid import UUID

from app.domain.models import (
    AnswerEvaluation,
    CandidateProfile,
    InterviewPlan,
    InterviewQuestion,
    InterviewTurn,
    JobAnalysis,
    SourceCitation,
)


class CandidateProfilingSkill(Protocol):
    async def build_candidate_profile(self, user_id: UUID, session_id: UUID) -> CandidateProfile:
        ...


class JDAnalysisSkill(Protocol):
    async def analyze_job_description(
        self,
        session_id: UUID,
        company_name: str,
        role_title: str,
        jd_text: str,
    ) -> JobAnalysis:
        ...


class CompanyResearchSkill(Protocol):
    async def research_company_and_role(
        self,
        company_name: str,
        role_title: str,
        jd_analysis: JobAnalysis,
    ) -> list[SourceCitation]:
        ...


class InterviewIntelSkill(Protocol):
    async def collect_interview_intel(
        self,
        company_name: str,
        role_title: str,
        topics: list[str],
    ) -> list[SourceCitation]:
        ...


class InterviewPlanningSkill(Protocol):
    async def create_interview_plan(
        self,
        session_id: UUID,
        candidate_profile: CandidateProfile,
        job_analysis: JobAnalysis,
        company_sources: list[SourceCitation],
        interview_intel: list[SourceCitation],
    ) -> InterviewPlan:
        ...


class LiveInterviewSkill(Protocol):
    async def select_next_question(
        self,
        session_id: UUID,
        plan: InterviewPlan,
        transcript: list[InterviewTurn],
    ) -> InterviewQuestion:
        ...

    async def decide_follow_up(
        self,
        session_id: UUID,
        current_question: InterviewQuestion,
        candidate_answer: str,
        transcript: list[InterviewTurn],
    ) -> InterviewQuestion | None:
        ...


class EvaluationSkill(Protocol):
    async def evaluate_answer(
        self,
        session_id: UUID,
        question: InterviewQuestion,
        candidate_answer: str,
    ) -> AnswerEvaluation:
        ...


class ReportGenerationSkill(Protocol):
    async def generate_final_report(
        self,
        session_id: UUID,
        transcript: list[InterviewTurn],
        evaluations: list[AnswerEvaluation],
    ) -> str:
        ...

