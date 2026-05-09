from app.domain.models import JobAnalysis, ResearchFinding
from app.skills.contracts import CompanyResearchSkill


class CompanyResearchAgent:
    def __init__(
        self,
        company_name: str,
        role_title: str,
        job_analysis: JobAnalysis,
        company_research_skill: CompanyResearchSkill,
    ) -> None:
        self.company_name = company_name
        self.role_title = role_title
        self.job_analysis = job_analysis
        self.company_research_skill = company_research_skill

    async def run(self) -> list[ResearchFinding]:
        return await self.company_research_skill.research_company_and_role(
            company_name=self.company_name,
            role_title=self.role_title,
            jd_analysis=self.job_analysis,
        )

