from typing import Any, Protocol
from uuid import UUID

from app.domain.models import MemoryKind, MemoryNamespace, MemoryRecord


class LongTermMemoryRepository(Protocol):
    async def save_memory(self, memory: MemoryRecord) -> UUID:
        ...

    async def save_memories(self, memories: list[MemoryRecord]) -> list[UUID]:
        ...

    async def get_memory(self, memory_id: UUID) -> MemoryRecord | None:
        ...

    async def list_memories(
        self,
        namespace: MemoryNamespace,
        kind: MemoryKind | None = None,
        limit: int = 50,
    ) -> list[MemoryRecord]:
        ...

    async def search_memories(
        self,
        namespace: MemoryNamespace,
        query_embedding: list[float],
        kind: MemoryKind | None = None,
        metadata_filters: dict[str, Any] | None = None,
        top_k: int = 10,
    ) -> list[MemoryRecord]:
        ...
