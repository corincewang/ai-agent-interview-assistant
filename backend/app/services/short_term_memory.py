from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from app.services.session_store import InterviewSessionRecord


def build_short_term_memory_config(session: InterviewSessionRecord) -> dict:
    return {"configurable": {"thread_id": session.short_term_memory.thread_id}}


def normalize_postgres_checkpoint_url(database_url: str) -> str:
    if database_url.startswith("postgresql+asyncpg://"):
        return "postgresql://" + database_url.removeprefix("postgresql+asyncpg://")
    if database_url.startswith("postgresql+psycopg://"):
        return "postgresql://" + database_url.removeprefix("postgresql+psycopg://")
    return database_url


@asynccontextmanager
async def postgres_short_term_checkpointer(
    database_url: str,
) -> AsyncIterator[object]:
    from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

    checkpoint_url = normalize_postgres_checkpoint_url(database_url)
    async with AsyncPostgresSaver.from_conn_string(checkpoint_url) as checkpointer:
        await checkpointer.setup()
        yield checkpointer
