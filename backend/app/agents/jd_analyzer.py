from uuid import UUID

from app.domain.models import JobAnalysis
from app.skills.contracts import JDAnalysisSkill


class JDAnalyzerAgent:
    def __init__(
        self,
        session_id: UUID,
        company_name: str,
        role_title: str,
        jd_text: str,
        jd_analysis_skill: JDAnalysisSkill,
    ) -> None:
        self.session_id = session_id
        self.company_name = company_name
        self.role_title = role_title
        self.jd_text = jd_text
        self.jd_analysis_skill = jd_analysis_skill

    async def run(self) -> JobAnalysis:
        return await self.jd_analysis_skill.analyze_job_description(
            session_id=self.session_id,
            company_name=self.company_name,
            role_title=self.role_title,
            jd_text=self.jd_text,
        )

