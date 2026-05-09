from uuid import UUID

from app.domain.models import CandidateProfile, ResumeProfile
from app.skills.contracts import CandidateProfilingSkill


class CandidateProfilerAgent:
    def __init__(
        self,
        user_id: UUID,
        session_id: UUID,
        resume_profile: ResumeProfile,
        candidate_profiling_skill: CandidateProfilingSkill,
    ) -> None:
        self.user_id = user_id
        self.session_id = session_id
        self.resume_profile = resume_profile
        self.candidate_profiling_skill = candidate_profiling_skill

    async def run(self) -> CandidateProfile:
        return await self.candidate_profiling_skill.build_candidate_profile(
            user_id=self.user_id,
            session_id=self.session_id,
            resume_profile=self.resume_profile,
        )

