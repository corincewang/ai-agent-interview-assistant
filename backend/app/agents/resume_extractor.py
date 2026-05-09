from uuid import UUID

from app.domain.models import ParsedDocument, ResumeProfile
from app.skills.contracts import ResumeExtractionSkill


class ResumeExtractorAgent:
    def __init__(
        self,
        user_id: UUID,
        parsed_resume: ParsedDocument,
        resume_extraction_skill: ResumeExtractionSkill,
    ) -> None:
        self.user_id = user_id
        self.parsed_resume = parsed_resume
        self.resume_extraction_skill = resume_extraction_skill

    async def run(self) -> ResumeProfile:
        return await self.resume_extraction_skill.extract_resume_profile(
            user_id=self.user_id,
            parsed_resume=self.parsed_resume,
        )

