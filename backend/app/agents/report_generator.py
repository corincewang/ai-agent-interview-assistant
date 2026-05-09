from uuid import UUID

from app.domain.models import AnswerEvaluation, InterviewTurn
from app.skills.contracts import ReportGenerationSkill


class ReportGeneratorAgent:
    def __init__(
        self,
        session_id: UUID,
        transcript: list[InterviewTurn],
        evaluations: list[AnswerEvaluation],
        report_generation_skill: ReportGenerationSkill,
    ) -> None:
        self.session_id = session_id
        self.transcript = transcript
        self.evaluations = evaluations
        self.report_generation_skill = report_generation_skill

    async def run(self) -> str:
        return await self.report_generation_skill.generate_final_report(
            session_id=self.session_id,
            transcript=self.transcript,
            evaluations=self.evaluations,
        )

