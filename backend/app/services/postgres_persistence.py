from collections.abc import Awaitable, Callable

from sqlalchemy.ext.asyncio import AsyncSession

from app.config.settings import Settings
from app.db.session import build_async_engine, build_session_factory, session_scope
from app.domain.models import DocumentInput
from app.repositories.documents import PostgresDocumentRepository
from app.repositories.interview_artifacts import PostgresInterviewArtifactRepository
from app.repositories.interview_sessions import PostgresInterviewSessionRepository
from app.repositories.session_summary import (
    InterviewSessionDatabaseSummary,
    PostgresSessionSummaryRepository,
)
from app.services.session_store import InterviewSessionRecord


class OptionalPostgresPersistence:
    def __init__(self, settings: Settings) -> None:
        self.database_url = settings.database_url
        self.enabled = self.database_url is not None

    async def _run_with_session(
        self,
        operation: Callable[[AsyncSession], Awaitable[None]],
    ) -> None:
        if self.database_url is None:
            return

        engine = build_async_engine(self.database_url)
        try:
            session_factory = build_session_factory(engine)
            async for db_session in session_scope(session_factory):
                await operation(db_session)
        finally:
            await engine.dispose()

    async def persist_session(
        self,
        session_record: InterviewSessionRecord,
        status: str = "created",
    ) -> None:
        try:
            async def operation(db_session: AsyncSession) -> None:
                repository = PostgresInterviewSessionRepository(db_session)
                await repository.upsert_session(session_record, status=status)

            await self._run_with_session(operation)
        except Exception as exc:
            print(f"Postgres persistence warning: session was not persisted: {exc}")

    async def persist_uploaded_document(
        self,
        session_record: InterviewSessionRecord,
        document_input: DocumentInput,
    ) -> None:
        try:
            async def operation(db_session: AsyncSession) -> None:
                session_repository = PostgresInterviewSessionRepository(db_session)
                document_repository = PostgresDocumentRepository(db_session)
                await session_repository.upsert_session(session_record)
                await document_repository.save_uploaded_document(
                    session_id=session_record.session_id,
                    document_input=document_input,
                )

            await self._run_with_session(operation)
        except Exception as exc:
            print(f"Postgres persistence warning: uploaded document was not persisted: {exc}")

    async def persist_prepared_session(
        self,
        session_record: InterviewSessionRecord,
    ) -> None:
        if session_record.prepared_state is None:
            return

        try:
            async def operation(db_session: AsyncSession) -> None:
                session_repository = PostgresInterviewSessionRepository(db_session)
                document_repository = PostgresDocumentRepository(db_session)
                artifact_repository = PostgresInterviewArtifactRepository(db_session)

                await session_repository.upsert_session(session_record, status="prepared")

                for document in session_record.prepared_state.get("parsed_documents", []):
                    await document_repository.save_parsed_document(
                        session_id=session_record.session_id,
                        document=document,
                    )

                indexed_document_ids = set()
                indexing_result = session_record.prepared_state.get("knowledge_indexing_result")
                if indexing_result is not None:
                    indexed_document_ids = set(indexing_result.indexed_document_ids)

                chunks_by_document_id = {}
                for chunk in session_record.prepared_state.get("document_chunks", []):
                    if chunk.document_id in indexed_document_ids:
                        continue
                    chunks_by_document_id.setdefault(chunk.document_id, []).append(chunk)

                for document_id, chunks in chunks_by_document_id.items():
                    await document_repository.replace_chunks(
                        session_id=session_record.session_id,
                        document_id=document_id,
                        chunks=chunks,
                    )

                if session_record.interview_plan is not None:
                    await artifact_repository.save_interview_plan(session_record.interview_plan)

            await self._run_with_session(operation)
        except Exception as exc:
            print(f"Postgres persistence warning: prepared session was not persisted: {exc}")

    async def persist_transcript(
        self,
        session_record: InterviewSessionRecord,
    ) -> None:
        try:
            async def operation(db_session: AsyncSession) -> None:
                artifact_repository = PostgresInterviewArtifactRepository(db_session)
                await artifact_repository.replace_turns(
                    session_id=session_record.session_id,
                    turns=session_record.transcript,
                )

            await self._run_with_session(operation)
        except Exception as exc:
            print(f"Postgres persistence warning: transcript was not persisted: {exc}")

    async def persist_evaluations(
        self,
        session_record: InterviewSessionRecord,
    ) -> None:
        try:
            async def operation(db_session: AsyncSession) -> None:
                artifact_repository = PostgresInterviewArtifactRepository(db_session)
                await artifact_repository.save_evaluations(
                    session_id=session_record.session_id,
                    evaluations=session_record.evaluations,
                )

            await self._run_with_session(operation)
        except Exception as exc:
            print(f"Postgres persistence warning: evaluations were not persisted: {exc}")

    async def persist_report(
        self,
        session_record: InterviewSessionRecord,
    ) -> None:
        if session_record.report is None:
            return

        try:
            async def operation(db_session: AsyncSession) -> None:
                artifact_repository = PostgresInterviewArtifactRepository(db_session)
                await artifact_repository.save_report(
                    session_id=session_record.session_id,
                    report=session_record.report,
                )

            await self._run_with_session(operation)
        except Exception as exc:
            print(f"Postgres persistence warning: report was not persisted: {exc}")

    async def get_session_summary(
        self,
        session_id,
    ) -> InterviewSessionDatabaseSummary | None:
        summary: InterviewSessionDatabaseSummary | None = None

        async def operation(db_session: AsyncSession) -> None:
            nonlocal summary
            repository = PostgresSessionSummaryRepository(db_session)
            summary = await repository.get_summary(session_id)

        await self._run_with_session(operation)
        return summary

    async def get_interview_plan_payload(self, session_id) -> dict | None:
        plan_payload: dict | None = None

        async def operation(db_session: AsyncSession) -> None:
            nonlocal plan_payload
            repository = PostgresInterviewArtifactRepository(db_session)
            plan_payload = await repository.get_interview_plan_payload(session_id)

        await self._run_with_session(operation)
        return plan_payload

    async def dispose(self) -> None:
        return None
