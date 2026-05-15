from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import InterviewSessionRecord as DBInterviewSessionRecord
from app.domain.models import InterviewMode
from app.services.session_store import InterviewSessionRecord


class PostgresInterviewSessionRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create_session(
        self,
        company_name: str,
        role_title: str,
        target_track: str,
        jd_text: str,
        mode: InterviewMode,
        user_id: UUID | None = None,
    ) -> InterviewSessionRecord:
        record = DBInterviewSessionRecord(
            user_id=user_id or uuid4(),
            company_name=company_name,
            role_title=role_title,
            target_track=target_track,
            jd_text=jd_text,
            mode=mode.value,
            status="created",
        )
        self.session.add(record)
        await self.session.flush()
        return _to_domain_session(record)

    async def upsert_session(
        self,
        session_record: InterviewSessionRecord,
        status: str = "created",
    ) -> None:
        record = await self.session.get(DBInterviewSessionRecord, session_record.session_id)
        if record is None:
            record = DBInterviewSessionRecord(
                id=session_record.session_id,
                user_id=session_record.user_id,
                company_name=session_record.company_name,
                role_title=session_record.role_title,
                target_track=session_record.target_track,
                jd_text=session_record.jd_text,
                mode=session_record.mode.value,
                status=status,
            )
            self.session.add(record)
        else:
            record.user_id = session_record.user_id
            record.company_name = session_record.company_name
            record.role_title = session_record.role_title
            record.target_track = session_record.target_track
            record.jd_text = session_record.jd_text
            record.mode = session_record.mode.value
            record.status = status

        await self.session.flush()

    async def get_session(self, session_id: UUID) -> InterviewSessionRecord | None:
        record = await self.session.get(DBInterviewSessionRecord, session_id)
        if record is None:
            return None
        return _to_domain_session(record)

    async def require_session(self, session_id: UUID) -> InterviewSessionRecord:
        session = await self.get_session(session_id)
        if session is None:
            raise KeyError(f"Interview session not found: {session_id}")
        return session

    async def update_status(self, session_id: UUID, status: str) -> None:
        record = await self.session.get(DBInterviewSessionRecord, session_id)
        if record is None:
            raise KeyError(f"Interview session not found: {session_id}")

        record.status = status
        await self.session.flush()

    async def list_sessions_for_user(self, user_id: UUID) -> list[InterviewSessionRecord]:
        result = await self.session.scalars(
            select(DBInterviewSessionRecord)
            .where(DBInterviewSessionRecord.user_id == user_id)
            .order_by(DBInterviewSessionRecord.created_at.desc())
        )
        return [_to_domain_session(record) for record in result]


def _to_domain_session(record: DBInterviewSessionRecord) -> InterviewSessionRecord:
    return InterviewSessionRecord(
        session_id=record.id,
        user_id=record.user_id,
        company_name=record.company_name,
        role_title=record.role_title,
        target_track=record.target_track,
        jd_text=record.jd_text,
        mode=InterviewMode(record.mode),
    )
