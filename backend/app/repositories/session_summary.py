from dataclasses import dataclass
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import (
    DocumentChunkRecord,
    DocumentRecord,
    InterviewPlanRecord,
    InterviewPlanCritiqueRecord,
    InterviewQuestionRecord,
    InterviewSessionRecord,
)


@dataclass(frozen=True)
class InterviewSessionDatabaseSummary:
    session_id: UUID
    company_name: str
    role_title: str
    status: str
    document_count: int
    parsed_document_count: int
    chunk_count: int
    embedded_chunk_count: int
    plan_count: int
    question_count: int
    critique_count: int
    critique_overall_score: float | None
    critique_quality_gate_passed: bool | None


class PostgresSessionSummaryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_summary(
        self,
        session_id: UUID,
    ) -> InterviewSessionDatabaseSummary | None:
        session_record = await self.session.get(InterviewSessionRecord, session_id)
        if session_record is None:
            return None

        document_count = await self._count(
            select(func.count())
            .select_from(DocumentRecord)
            .where(DocumentRecord.session_id == session_id)
        )
        parsed_document_count = await self._count(
            select(func.count())
            .select_from(DocumentRecord)
            .where(DocumentRecord.session_id == session_id)
            .where(DocumentRecord.document_metadata["upload_status"].astext == "parsed")
        )
        chunk_count = await self._count(
            select(func.count())
            .select_from(DocumentChunkRecord)
            .where(DocumentChunkRecord.session_id == session_id)
        )
        embedded_chunk_count = await self._count(
            select(func.count())
            .select_from(DocumentChunkRecord)
            .where(DocumentChunkRecord.session_id == session_id)
            .where(DocumentChunkRecord.embedding.is_not(None))
        )
        plan_count = await self._count(
            select(func.count())
            .select_from(InterviewPlanRecord)
            .where(InterviewPlanRecord.session_id == session_id)
        )
        question_count = await self._count(
            select(func.count())
            .select_from(InterviewQuestionRecord)
            .join(InterviewPlanRecord)
            .where(InterviewPlanRecord.session_id == session_id)
        )
        critique_record = await self.session.scalar(
            select(InterviewPlanCritiqueRecord).where(
                InterviewPlanCritiqueRecord.session_id == session_id
            )
        )

        return InterviewSessionDatabaseSummary(
            session_id=session_record.id,
            company_name=session_record.company_name,
            role_title=session_record.role_title,
            status=session_record.status,
            document_count=document_count,
            parsed_document_count=parsed_document_count,
            chunk_count=chunk_count,
            embedded_chunk_count=embedded_chunk_count,
            plan_count=plan_count,
            question_count=question_count,
            critique_count=1 if critique_record is not None else 0,
            critique_overall_score=(
                critique_record.overall_score if critique_record is not None else None
            ),
            critique_quality_gate_passed=(
                critique_record.quality_gate_passed if critique_record is not None else None
            ),
        )

    async def _count(self, statement) -> int:
        return int(await self.session.scalar(statement) or 0)
