from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import (
    AnswerEvaluationRecord,
    InterviewPlanRecord,
    InterviewPlanCritiqueRecord,
    InterviewQuestionRecord,
    InterviewTurnRecord,
    QuestionCritiqueRecord,
    ReportRecord,
)
from app.domain.models import (
    AnswerEvaluation,
    InterviewPlan,
    InterviewPlanCritique,
    InterviewTurn,
)
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
                    question_metadata=to_jsonable(
                        {
                            "question_type": (
                                question.question_type.value
                                if question.question_type is not None
                                else None
                            ),
                            "source_scope": (
                                question.source_scope.value
                                if question.source_scope is not None
                                else None
                            ),
                            "why_asked": question.why_asked,
                            "evidence_chunk_ids": [
                                str(chunk_id) for chunk_id in question.evidence_chunk_ids
                            ],
                        }
                    ),
                )
                for index, question in enumerate(plan.questions, start=1)
            ]
        )
        await self.session.flush()
        return plan_record.id

    async def save_interview_plan_critique(
        self,
        critique: InterviewPlanCritique,
    ) -> UUID:
        await self.session.execute(
            delete(InterviewPlanCritiqueRecord).where(
                InterviewPlanCritiqueRecord.session_id == critique.session_id
            )
        )

        plan_record = await self.session.scalar(
            select(InterviewPlanRecord).where(
                InterviewPlanRecord.session_id == critique.session_id
            )
        )
        plan_id = plan_record.id if plan_record is not None else None

        critique_record = InterviewPlanCritiqueRecord(
            session_id=critique.session_id,
            plan_id=plan_id,
            overall_score=critique.overall_score,
            quality_gate_passed=critique.quality_gate_passed,
            coverage_summary=to_jsonable(critique.coverage_summary),
            revision_recommendations=to_jsonable(critique.revision_recommendations),
            web_intel_risk_notes=to_jsonable(critique.web_intel_risk_notes),
            critique_payload=to_jsonable(critique),
        )
        self.session.add(critique_record)
        await self.session.flush()

        self.session.add_all(
            [
                QuestionCritiqueRecord(
                    plan_critique_id=critique_record.id,
                    question_id=question_critique.question_id,
                    resume_grounding_score=question_critique.resume_grounding_score,
                    jd_coverage_score=question_critique.jd_coverage_score,
                    rag_grounding_score=question_critique.rag_grounding_score,
                    specificity_score=question_critique.specificity_score,
                    follow_up_potential_score=question_critique.follow_up_potential_score,
                    overall_score=question_critique.overall_score,
                    strengths=to_jsonable(question_critique.strengths),
                    improvement_suggestions=to_jsonable(
                        question_critique.improvement_suggestions
                    ),
                )
                for question_critique in critique.question_critiques
            ]
        )
        await self.session.flush()
        return critique_record.id

    async def get_interview_plan_payload(self, session_id: UUID) -> dict | None:
        result = await self.session.scalar(
            select(InterviewPlanRecord.plan_payload).where(
                InterviewPlanRecord.session_id == session_id
            )
        )
        return result

    async def get_interview_plan_critique_payload(self, session_id: UUID) -> dict | None:
        result = await self.session.scalar(
            select(InterviewPlanCritiqueRecord.critique_payload).where(
                InterviewPlanCritiqueRecord.session_id == session_id
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
