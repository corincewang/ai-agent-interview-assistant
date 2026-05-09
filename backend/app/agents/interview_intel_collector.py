from app.domain.models import ResearchFinding
from app.skills.contracts import InterviewIntelSkill


class InterviewIntelAgent:
    def __init__(
        self,
        company_name: str,
        role_title: str,
        topics: list[str],
        interview_intel_skill: InterviewIntelSkill,
    ) -> None:
        self.company_name = company_name
        self.role_title = role_title
        self.topics = topics
        self.interview_intel_skill = interview_intel_skill

    async def run(self) -> list[ResearchFinding]:
        return await self.interview_intel_skill.collect_interview_intel(
            company_name=self.company_name,
            role_title=self.role_title,
            topics=self.topics,
        )

