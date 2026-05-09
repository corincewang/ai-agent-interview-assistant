from typing import Protocol
from uuid import UUID

from app.domain.models import (
    AnswerEvaluation,
    CandidateJobMatch,
    CandidateProfile,
    InterviewPlan,
    InterviewQuestion,
    InterviewTurn,
    JobAnalysis,
    ParsedDocument,
    ResearchFinding,
    ResumeProfile,
    SourceCitation,
)


class ResumeExtractionSkill(Protocol):
    """Extract objective resume facts from a parsed resume document."""

    async def extract_resume_profile(
        self,
        user_id: UUID,
        parsed_resume: ParsedDocument,
    ) -> ResumeProfile:
        ...


class CandidateProfilingSkill(Protocol):
    """Turn objective resume facts into an interview-oriented candidate profile."""

    async def build_candidate_profile(
        self,
        user_id: UUID,
        session_id: UUID,
        resume_profile: ResumeProfile,
    ) -> CandidateProfile:
        ...


class JDAnalysisSkill(Protocol):
    """Extract objective role requirements from a job description."""

    async def analyze_job_description(
        self,
        session_id: UUID,
        company_name: str,
        role_title: str,
        jd_text: str,
    ) -> JobAnalysis:
        ...


class CandidateJobMatchingSkill(Protocol):
    """Compare a candidate profile against a role and produce session-specific fit analysis."""

    async def match_candidate_to_job(
        self,
        session_id: UUID,
        candidate_profile: CandidateProfile,
        job_analysis: JobAnalysis,
    ) -> CandidateJobMatch:
        ...


class CompanyResearchSkill(Protocol):
    """Collect public company and role context with citation metadata."""

    async def research_company_and_role(
        self,
        company_name: str,
        role_title: str,
        jd_analysis: JobAnalysis,
    ) -> list[ResearchFinding]:
        ...


class InterviewIntelSkill(Protocol):
    """Collect public interview experience signals and estimate their relevance."""

    async def collect_interview_intel(
        self,
        company_name: str,
        role_title: str,
        topics: list[str],
    ) -> list[ResearchFinding]:
        ...


class InterviewPlanningSkill(Protocol):
    """Create the interview plan from candidate, role, match, company, and interview intel."""

    async def create_interview_plan(
        self,
        session_id: UUID,
        candidate_profile: CandidateProfile,
        job_analysis: JobAnalysis,
        candidate_job_match: CandidateJobMatch,
        company_sources: list[ResearchFinding],
        interview_intel: list[ResearchFinding],
    ) -> InterviewPlan:
        ...


class LiveInterviewSkill(Protocol):
    """Run low-latency interview turns and decide whether to ask follow-up questions."""

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
    """Evaluate candidate answers against question-specific and role-specific rubrics."""

    async def evaluate_answer(
        self,
        session_id: UUID,
        question: InterviewQuestion,
        candidate_answer: str,
    ) -> AnswerEvaluation:
        ...


class ReportGenerationSkill(Protocol):
    """Generate the final feedback report and next-step practice plan."""

    async def generate_final_report(
        self,
        session_id: UUID,
        transcript: list[InterviewTurn],
        evaluations: list[AnswerEvaluation],
    ) -> str:
        ...
