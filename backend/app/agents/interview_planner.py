from uuid import UUID

from app.domain.models import (
    CandidateJobMatch,
    CandidateProfile,
    InterviewPlan,
    JobAnalysis,
    SourceCitation,
)
from app.skills.contracts import InterviewPlanningSkill


class InterviewPlannerAgent:
    def __init__(
        self,
        session_id: UUID,
        candidate_profile: CandidateProfile,
        job_analysis: JobAnalysis,
        candidate_job_match: CandidateJobMatch,
        company_sources: list[SourceCitation],
        interview_intel: list[SourceCitation],
        interview_planning_skill: InterviewPlanningSkill,
    ) -> None:
        self.session_id = session_id
        self.candidate_profile = candidate_profile
        self.job_analysis = job_analysis
        self.candidate_job_match = candidate_job_match
        self.company_sources = company_sources
        self.interview_intel = interview_intel
        self.interview_planning_skill = interview_planning_skill

    async def run(self) -> InterviewPlan:
        return await self.interview_planning_skill.create_interview_plan(
            session_id=self.session_id,
            candidate_profile=self.candidate_profile,
            job_analysis=self.job_analysis,
            candidate_job_match=self.candidate_job_match,
            company_sources=self.company_sources,
            interview_intel=self.interview_intel,
        )

