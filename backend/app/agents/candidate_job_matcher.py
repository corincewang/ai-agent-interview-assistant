from uuid import UUID

from app.domain.models import CandidateJobMatch, CandidateProfile, JobAnalysis
from app.skills.contracts import CandidateJobMatchingSkill


class CandidateJobMatcherAgent:
    def __init__(
        self,
        session_id: UUID,
        candidate_profile: CandidateProfile,
        job_analysis: JobAnalysis,
        candidate_job_matching_skill: CandidateJobMatchingSkill,
    ) -> None:
        self.session_id = session_id
        self.candidate_profile = candidate_profile
        self.job_analysis = job_analysis
        self.candidate_job_matching_skill = candidate_job_matching_skill

    async def run(self) -> CandidateJobMatch:
        return await self.candidate_job_matching_skill.match_candidate_to_job(
            session_id=self.session_id,
            candidate_profile=self.candidate_profile,
            job_analysis=self.job_analysis,
        )

