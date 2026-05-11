import asyncio
from uuid import uuid4

from app.config.settings import load_settings
from app.db.session import build_async_engine, build_session_factory, session_scope
from app.domain.models import (
    AnswerEvaluation,
    DocumentChunk,
    DocumentType,
    EmbeddedDocumentChunk,
    InterviewMode,
    InterviewPlan,
    InterviewQuestion,
    InterviewTurn,
    InterviewTurnRole,
    ParsedDocument,
)
from app.repositories.documents import PostgresDocumentRepository
from app.repositories.interview_artifacts import PostgresInterviewArtifactRepository
from app.repositories.interview_sessions import PostgresInterviewSessionRepository
from app.tools.postgres_vector_store import PostgresVectorStore


async def main() -> None:
    settings = load_settings()
    if settings.database_url is None:
        print("DATABASE_URL is required to run the persistence demo.")
        return

    engine = build_async_engine(settings.database_url)
    session_factory = build_session_factory(engine)

    async for db_session in session_scope(session_factory):
        session_repository = PostgresInterviewSessionRepository(db_session)
        document_repository = PostgresDocumentRepository(db_session)
        artifact_repository = PostgresInterviewArtifactRepository(db_session)
        vector_store = PostgresVectorStore(db_session)

        interview_session = await session_repository.create_session(
            company_name="Persistence Demo Company",
            role_title="AI Agent Engineer",
            jd_text="Build AI agent interview workflows with RAG and PostgreSQL.",
            mode=InterviewMode.AI_AGENT,
        )

        document = ParsedDocument(
            id=uuid4(),
            document_type=DocumentType.KNOWLEDGE_BASE,
            raw_text="RAG indexing stores chunks. Retrieval searches top-k matching chunks.",
            source_spans=[],
            metadata={"file_name": "demo.md", "file_suffix": ".md"},
        )
        await document_repository.save_parsed_document(
            session_id=interview_session.session_id,
            document=document,
            file_path=None,
        )

        chunks = [
            EmbeddedDocumentChunk(
                chunk=DocumentChunk(
                    id=uuid4(),
                    document_id=document.id,
                    text="RAG indexing stores knowledge-base chunks with embedding metadata.",
                    metadata={
                        "document_type": DocumentType.KNOWLEDGE_BASE.value,
                        "chunk_index": 0,
                        "start_char": 0,
                        "end_char": 68,
                    },
                ),
                embedding=_demo_embedding(0.9),
                embedding_model="demo-embedding",
            ),
            EmbeddedDocumentChunk(
                chunk=DocumentChunk(
                    id=uuid4(),
                    document_id=document.id,
                    text="Frontend rendering performance can be improved with memoization.",
                    metadata={
                        "document_type": DocumentType.KNOWLEDGE_BASE.value,
                        "chunk_index": 1,
                        "start_char": 69,
                        "end_char": 134,
                    },
                ),
                embedding=_demo_embedding(0.1),
                embedding_model="demo-embedding",
            ),
        ]
        await vector_store.upsert_chunks(
            session_id=interview_session.session_id,
            chunks=chunks,
        )

        question = InterviewQuestion(
            id=uuid4(),
            prompt="How would you design RAG indexing and retrieval for this assistant?",
            topic="RAG Architecture",
            difficulty="medium",
            expected_signals=["indexing/retrieval split", "top-k search", "metadata"],
            follow_up_strategy=["Ask about pgvector migration."],
        )
        plan = InterviewPlan(
            session_id=interview_session.session_id,
            mode=InterviewMode.AI_AGENT,
            questions=[question],
            rubric={"depth": "Explains tradeoffs clearly."},
            candidate_storyline="Candidate can explain RAG infrastructure.",
            planned_deep_dives=["RAG", "PostgreSQL", "pgvector"],
        )
        await artifact_repository.save_interview_plan(plan)

        turn = InterviewTurn(
            session_id=interview_session.session_id,
            role=InterviewTurnRole.CANDIDATE,
            content="I would split indexing and retrieval.",
            metadata={"question_id": str(question.id)},
        )
        turn_id = await artifact_repository.save_turn(turn)
        await artifact_repository.save_evaluations(
            session_id=interview_session.session_id,
            evaluations=[
                AnswerEvaluation(
                    turn_id=turn_id,
                    scores={"depth": 8},
                    strengths=["Clear architecture split."],
                    weaknesses=["Could discuss reranking."],
                    improved_answer="I would add metadata filters and reranking.",
                    next_practice_steps=["Practice pgvector query explanation."],
                )
            ],
        )
        await artifact_repository.save_report(
            session_id=interview_session.session_id,
            report="Persistence demo report.",
        )

        retrieved = await vector_store.search(
            session_id=interview_session.session_id,
            query_embedding=_demo_embedding(1.0),
            top_k=1,
            document_types=[DocumentType.KNOWLEDGE_BASE],
        )

        print(
            {
                "session_id": str(interview_session.session_id),
                "retrieved_count": len(retrieved),
                "top_chunk": retrieved[0].chunk.text if retrieved else None,
                "top_score": round(retrieved[0].score, 4) if retrieved else None,
            }
        )

    await engine.dispose()


def _demo_embedding(signal: float) -> list[float]:
    return [signal, 1.0 - signal] + [0.0] * 1534


if __name__ == "__main__":
    asyncio.run(main())
