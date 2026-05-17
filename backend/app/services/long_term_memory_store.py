from collections.abc import Awaitable, Callable
from typing import Any
from uuid import UUID

from app.config.settings import Settings
from app.db.session import build_async_engine, build_session_factory, session_scope
from app.domain.models import MemoryKind, MemoryNamespace, MemoryRecord
from app.ports.memory import LongTermMemoryRepository
from app.repositories.memory import (
    InMemoryLongTermMemoryRepository,
    PostgresLongTermMemoryRepository,
)


class LongTermMemoryStore:
    def __init__(
        self,
        settings: Settings,
        fallback_repository: LongTermMemoryRepository | None = None,
    ) -> None:
        self.database_url = settings.database_url
        self.fallback_repository = (
            fallback_repository or InMemoryLongTermMemoryRepository()
        )

    async def save_memory(self, memory: MemoryRecord) -> UUID:
        ids = await self.save_memories([memory])
        return ids[0]

    async def save_memories(self, memories: list[MemoryRecord]) -> list[UUID]:
        if self.database_url is None:
            return await self.fallback_repository.save_memories(memories)

        async def operation(repository: PostgresLongTermMemoryRepository) -> list[UUID]:
            return await repository.save_memories(memories)

        return await self._run_with_postgres(operation)

    async def get_memory(self, memory_id: UUID) -> MemoryRecord | None:
        if self.database_url is None:
            return await self.fallback_repository.get_memory(memory_id)

        async def operation(
            repository: PostgresLongTermMemoryRepository,
        ) -> MemoryRecord | None:
            return await repository.get_memory(memory_id)

        return await self._run_with_postgres(operation)

    async def list_memories(
        self,
        namespace: MemoryNamespace,
        kind: MemoryKind | None = None,
        limit: int = 50,
    ) -> list[MemoryRecord]:
        if self.database_url is None:
            return await self.fallback_repository.list_memories(
                namespace=namespace,
                kind=kind,
                limit=limit,
            )

        async def operation(
            repository: PostgresLongTermMemoryRepository,
        ) -> list[MemoryRecord]:
            return await repository.list_memories(
                namespace=namespace,
                kind=kind,
                limit=limit,
            )

        return await self._run_with_postgres(operation)

    async def search_memories(
        self,
        namespace: MemoryNamespace,
        query_embedding: list[float],
        kind: MemoryKind | None = None,
        metadata_filters: dict[str, Any] | None = None,
        top_k: int = 10,
    ) -> list[MemoryRecord]:
        if self.database_url is None:
            return await self.fallback_repository.search_memories(
                namespace=namespace,
                query_embedding=query_embedding,
                kind=kind,
                metadata_filters=metadata_filters,
                top_k=top_k,
            )

        async def operation(
            repository: PostgresLongTermMemoryRepository,
        ) -> list[MemoryRecord]:
            return await repository.search_memories(
                namespace=namespace,
                query_embedding=query_embedding,
                kind=kind,
                metadata_filters=metadata_filters,
                top_k=top_k,
            )

        return await self._run_with_postgres(operation)

    async def _run_with_postgres(
        self,
        operation: Callable[[PostgresLongTermMemoryRepository], Awaitable[Any]],
    ) -> Any:
        if self.database_url is None:
            raise ValueError("DATABASE_URL is required for PostgreSQL long-term memory")

        engine = build_async_engine(self.database_url)
        try:
            session_factory = build_session_factory(engine)
            async for db_session in session_scope(session_factory):
                repository = PostgresLongTermMemoryRepository(db_session)
                return await operation(repository)
        finally:
            await engine.dispose()

        raise RuntimeError("Long-term memory operation did not run")
