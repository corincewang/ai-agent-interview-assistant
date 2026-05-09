from uuid import UUID

from app.domain.models import AnswerEvaluation, InterviewQuestion
from app.skills.contracts import EvaluationSkill


class EvaluatorAgent:
    def __init__(
        self,
        session_id: UUID,
        question: InterviewQuestion,
        candidate_answer: str,
        evaluation_skill: EvaluationSkill,
    ) -> None:
        self.session_id = session_id
        self.question = question
        self.candidate_answer = candidate_answer
        self.evaluation_skill = evaluation_skill

    async def run(self) -> AnswerEvaluation:
        return await self.evaluation_skill.evaluate_answer(
            session_id=self.session_id,
            question=self.question,
            candidate_answer=self.candidate_answer,
        )

