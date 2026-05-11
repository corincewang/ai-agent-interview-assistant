from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import (
    AnswerEvaluationRecord,
    InterviewPlanRecord,
    InterviewQuestionRecord,
    InterviewTurnRecord,
    ReportRecord,
)
from app.domain.models import AnswerEvaluation, InterviewPlan, InterviewTurn
from app.utils.serialization import to_jsonable


class PostgresInterviewArtifactRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_interview_plan(self, plan: InterviewPlan) -> UUID:
        await self.session.execute(
            delete(InterviewPlanRecord).where(
                InterviewPlanRecord.session_id == plan.session_id
            )
        )

        plan_record = InterviewPlanRecord(
            session_id=plan.session_id,
            mode=plan.mode.value,
            candidate_storyline=plan.candidate_storyline,
            rubric=to_jsonable(plan.rubric),
            planned_deep_dives=to_jsonable(plan.planned_deep_dives),
            plan_payload=to_jsonable(plan),
        )
        self.session.add(plan_record)
        await self.session.flush()

        self.session.add_all(
            [
                InterviewQuestionRecord(
                    id=question.id,
                    plan_id=plan_record.id,
                    position=index,
                    prompt=question.prompt,
                    topic=question.topic,
                    difficulty=question.difficulty,
                    expected_signals=to_jsonable(question.expected_signals),
                    follow_up_strategy=to_jsonable(question.follow_up_strategy),
                )
                for index, question in enumerate(plan.questions, start=1)
            ]
        )
        await self.session.flush()
        return plan_record.id

    async def get_interview_plan_payload(self, session_id: UUID) -> dict | None:
        result = await self.session.scalar(
            select(InterviewPlanRecord.plan_payload).where(
                InterviewPlanRecord.session_id == session_id
            )
        )
        return result

    async def save_turn(self, turn: InterviewTurn) -> UUID:
        record = InterviewTurnRecord(
            session_id=turn.session_id,
            role=turn.role.value,
            content=turn.content,
            turn_metadata=to_jsonable(turn.metadata),
        )
        self.session.add(record)
        await self.session.flush()
        return record.id

    async def replace_turns(
        self,
        session_id: UUID,
        turns: list[InterviewTurn],
    ) -> list[UUID]:
        await self.session.execute(
            delete(InterviewTurnRecord).where(InterviewTurnRecord.session_id == session_id)
        )

        records = [
            InterviewTurnRecord(
                session_id=turn.session_id,
                role=turn.role.value,
                content=turn.content,
                turn_metadata=to_jsonable(turn.metadata),
            )
            for turn in turns
        ]
        self.session.add_all(records)
        await self.session.flush()
        return [record.id for record in records]

    async def save_evaluations(
        self,
        session_id: UUID,
        evaluations: list[AnswerEvaluation],
        preserve_turn_ids: bool = False,
    ) -> list[UUID]:
        await self.session.execute(
            delete(AnswerEvaluationRecord).where(
                AnswerEvaluationRecord.session_id == session_id
            )
        )

        records = [
            AnswerEvaluationRecord(
                turn_id=evaluation.turn_id if preserve_turn_ids else None,
                session_id=session_id,
                question_id=None,
                scores=to_jsonable(evaluation.scores),
                strengths=to_jsonable(evaluation.strengths),
                weaknesses=to_jsonable(evaluation.weaknesses),
                improved_answer=evaluation.improved_answer,
                next_practice_steps=to_jsonable(evaluation.next_practice_steps),
            )
            for evaluation in evaluations
        ]
        self.session.add_all(records)
        await self.session.flush()
        return [record.id for record in records]

    async def save_report(self, session_id: UUID, report: str) -> UUID:
        existing = await self.session.scalar(
            select(ReportRecord).where(ReportRecord.session_id == session_id)
        )
        if existing is None:
            existing = ReportRecord(session_id=session_id, report=report)
            self.session.add(existing)
        else:
            existing.report = report

        await self.session.flush()
        return existing.id

    async def get_report(self, session_id: UUID) -> str | None:
        return await self.session.scalar(
            select(ReportRecord.report).where(ReportRecord.session_id == session_id)
        )
