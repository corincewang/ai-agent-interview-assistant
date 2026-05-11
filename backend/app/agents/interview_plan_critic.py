from uuid import UUID

from app.domain.models import (
    CandidateJobMatch,
    CandidateProfile,
    InterviewPlan,
    InterviewPlanCritique,
    JobAnalysis,
    KnowledgeRetrievalResult,
)
from app.skills.contracts import InterviewPlanCriticSkill


class InterviewPlanCriticAgent:
    def __init__(
        self,
        session_id: UUID,
        interview_plan: InterviewPlan,
        candidate_profile: CandidateProfile,
        job_analysis: JobAnalysis,
        candidate_job_match: CandidateJobMatch,
        interview_plan_critic_skill: InterviewPlanCriticSkill,
        knowledge_context: KnowledgeRetrievalResult | None = None,
    ) -> None:
        self.session_id = session_id
        self.interview_plan = interview_plan
        self.candidate_profile = candidate_profile
        self.job_analysis = job_analysis
        self.candidate_job_match = candidate_job_match
        self.interview_plan_critic_skill = interview_plan_critic_skill
        self.knowledge_context = knowledge_context

    async def run(self) -> InterviewPlanCritique:
        return await self.interview_plan_critic_skill.critique_interview_plan(
            session_id=self.session_id,
            interview_plan=self.interview_plan,
            candidate_profile=self.candidate_profile,
            job_analysis=self.job_analysis,
            candidate_job_match=self.candidate_job_match,
            knowledge_context=self.knowledge_context,
        )
