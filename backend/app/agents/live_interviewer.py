from uuid import UUID

from app.domain.models import InterviewPlan, InterviewQuestion, InterviewTurn
from app.skills.contracts import LiveInterviewSkill


class LiveInterviewerAgent:
    def __init__(
        self,
        session_id: UUID,
        plan: InterviewPlan,
        transcript: list[InterviewTurn],
        live_interview_skill: LiveInterviewSkill,
    ) -> None:
        self.session_id = session_id
        self.plan = plan
        self.transcript = transcript
        self.live_interview_skill = live_interview_skill

    async def select_next_question(self) -> InterviewQuestion:
        return await self.live_interview_skill.select_next_question(
            session_id=self.session_id,
            plan=self.plan,
            transcript=self.transcript,
        )

    async def decide_follow_up(
        self,
        current_question: InterviewQuestion,
        candidate_answer: str,
    ) -> InterviewQuestion | None:
        return await self.live_interview_skill.decide_follow_up(
            session_id=self.session_id,
            current_question=current_question,
            candidate_answer=candidate_answer,
            transcript=self.transcript,
        )

