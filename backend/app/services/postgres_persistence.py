from app.config.settings import Settings
from app.db.session import build_async_engine, build_session_factory, session_scope
from app.repositories.documents import PostgresDocumentRepository
from app.repositories.interview_artifacts import PostgresInterviewArtifactRepository
from app.repositories.interview_sessions import PostgresInterviewSessionRepository
from app.services.session_store import InterviewSessionRecord


class OptionalPostgresPersistence:
    def __init__(self, settings: Settings) -> None:
        self.enabled = settings.database_url is not None
        self._engine = build_async_engine(settings.database_url) if settings.database_url else None
        self._session_factory = (
            build_session_factory(self._engine) if self._engine is not None else None
        )

    async def persist_session(
        self,
        session_record: InterviewSessionRecord,
        status: str = "created",
    ) -> None:
        if self._session_factory is None:
            return

        try:
            async for db_session in session_scope(self._session_factory):
                repository = PostgresInterviewSessionRepository(db_session)
                await repository.upsert_session(session_record, status=status)
        except Exception as exc:
            print(f"Postgres persistence warning: session was not persisted: {exc}")

    async def persist_prepared_session(
        self,
        session_record: InterviewSessionRecord,
    ) -> None:
        if self._session_factory is None or session_record.prepared_state is None:
            return

        try:
            async for db_session in session_scope(self._session_factory):
                session_repository = PostgresInterviewSessionRepository(db_session)
                document_repository = PostgresDocumentRepository(db_session)
                artifact_repository = PostgresInterviewArtifactRepository(db_session)

                await session_repository.upsert_session(session_record, status="prepared")

                for document in session_record.prepared_state.get("parsed_documents", []):
                    await document_repository.save_parsed_document(
                        session_id=session_record.session_id,
                        document=document,
                    )

                chunks_by_document_id = {}
                for chunk in session_record.prepared_state.get("document_chunks", []):
                    chunks_by_document_id.setdefault(chunk.document_id, []).append(chunk)

                for document_id, chunks in chunks_by_document_id.items():
                    await document_repository.replace_chunks(
                        session_id=session_record.session_id,
                        document_id=document_id,
                        chunks=chunks,
                    )

                if session_record.interview_plan is not None:
                    await artifact_repository.save_interview_plan(session_record.interview_plan)
        except Exception as exc:
            print(f"Postgres persistence warning: prepared session was not persisted: {exc}")

    async def persist_transcript(
        self,
        session_record: InterviewSessionRecord,
    ) -> None:
        if self._session_factory is None:
            return

        try:
            async for db_session in session_scope(self._session_factory):
                artifact_repository = PostgresInterviewArtifactRepository(db_session)
                await artifact_repository.replace_turns(
                    session_id=session_record.session_id,
                    turns=session_record.transcript,
                )
        except Exception as exc:
            print(f"Postgres persistence warning: transcript was not persisted: {exc}")

    async def persist_evaluations(
        self,
        session_record: InterviewSessionRecord,
    ) -> None:
        if self._session_factory is None:
            return

        try:
            async for db_session in session_scope(self._session_factory):
                artifact_repository = PostgresInterviewArtifactRepository(db_session)
                await artifact_repository.save_evaluations(
                    session_id=session_record.session_id,
                    evaluations=session_record.evaluations,
                )
        except Exception as exc:
            print(f"Postgres persistence warning: evaluations were not persisted: {exc}")

    async def persist_report(
        self,
        session_record: InterviewSessionRecord,
    ) -> None:
        if self._session_factory is None or session_record.report is None:
            return

        try:
            async for db_session in session_scope(self._session_factory):
                artifact_repository = PostgresInterviewArtifactRepository(db_session)
                await artifact_repository.save_report(
                    session_id=session_record.session_id,
                    report=session_record.report,
                )
        except Exception as exc:
            print(f"Postgres persistence warning: report was not persisted: {exc}")

    async def dispose(self) -> None:
        if self._engine is not None:
            await self._engine.dispose()
