import math
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import LongTermMemoryRecord
from app.domain.models import MemoryKind, MemoryNamespace, MemoryRecord, MemoryScope


class InMemoryLongTermMemoryRepository:
    def __init__(self) -> None:
        self._records: dict[UUID, MemoryRecord] = {}

    async def save_memory(self, memory: MemoryRecord) -> UUID:
        self._records[memory.id] = memory
        return memory.id

    async def save_memories(self, memories: list[MemoryRecord]) -> list[UUID]:
        ids: list[UUID] = []
        for memory in memories:
            ids.append(await self.save_memory(memory))
        return ids

    async def get_memory(self, memory_id: UUID) -> MemoryRecord | None:
        return self._records.get(memory_id)

    async def list_memories(
        self,
        namespace: MemoryNamespace,
        kind: MemoryKind | None = None,
        limit: int = 50,
    ) -> list[MemoryRecord]:
        if limit <= 0:
            return []

        matches = [
            memory
            for memory in self._records.values()
            if memory.namespace == namespace and _matches_kind(memory, kind)
        ]
        return matches[:limit]

    async def search_memories(
        self,
        namespace: MemoryNamespace,
        query_embedding: list[float],
        kind: MemoryKind | None = None,
        metadata_filters: dict[str, object] | None = None,
        top_k: int = 10,
    ) -> list[MemoryRecord]:
        if top_k <= 0:
            return []

        scored_records: list[tuple[float, MemoryRecord]] = []
        for memory in self._records.values():
            if memory.namespace != namespace:
                continue
            if not _matches_kind(memory, kind):
                continue
            if metadata_filters and not _matches_metadata(memory, metadata_filters):
                continue
            if memory.embedding is None:
                continue

            score = _cosine_similarity(query_embedding, memory.embedding)
            scored_records.append((score, memory))

        scored_records.sort(key=lambda item: item[0], reverse=True)
        return [memory for _, memory in scored_records[:top_k]]


def _matches_kind(memory: MemoryRecord, kind: MemoryKind | None) -> bool:
    return kind is None or memory.kind == kind


def _matches_metadata(
    memory: MemoryRecord,
    metadata_filters: dict[str, object],
) -> bool:
    for key, value in metadata_filters.items():
        if memory.metadata.get(key) != value:
            return False
    return True


def _cosine_similarity(left: list[float], right: list[float]) -> float:
    if not left or not right or len(left) != len(right):
        return 0.0

    dot_product = sum(left_value * right_value for left_value, right_value in zip(left, right))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))

    if left_norm == 0.0 or right_norm == 0.0:
        return 0.0

    return dot_product / (left_norm * right_norm)


class PostgresLongTermMemoryRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save_memory(self, memory: MemoryRecord) -> UUID:
        record = await self.session.get(LongTermMemoryRecord, memory.id)
        if record is None:
            record = LongTermMemoryRecord(id=memory.id)
            self.session.add(record)

        _apply_memory_to_record(record, memory)
        await self.session.flush()
        return memory.id

    async def save_memories(self, memories: list[MemoryRecord]) -> list[UUID]:
        ids: list[UUID] = []
        for memory in memories:
            ids.append(await self.save_memory(memory))
        return ids

    async def get_memory(self, memory_id: UUID) -> MemoryRecord | None:
        record = await self.session.get(LongTermMemoryRecord, memory_id)
        if record is None:
            return None
        return _record_to_memory(record)

    async def list_memories(
        self,
        namespace: MemoryNamespace,
        kind: MemoryKind | None = None,
        limit: int = 50,
    ) -> list[MemoryRecord]:
        if limit <= 0:
            return []

        statement = (
            select(LongTermMemoryRecord)
            .where(LongTermMemoryRecord.namespace_key == namespace.key)
            .order_by(LongTermMemoryRecord.created_at.desc())
            .limit(limit)
        )
        if kind is not None:
            statement = statement.where(LongTermMemoryRecord.kind == kind.value)

        records = await self.session.scalars(statement)
        return [_record_to_memory(record) for record in records]

    async def search_memories(
        self,
        namespace: MemoryNamespace,
        query_embedding: list[float],
        kind: MemoryKind | None = None,
        metadata_filters: dict[str, object] | None = None,
        top_k: int = 10,
    ) -> list[MemoryRecord]:
        if top_k <= 0:
            return []
        if not query_embedding:
            return await self.list_memories(namespace=namespace, kind=kind, limit=top_k)

        distance = LongTermMemoryRecord.embedding.cosine_distance(query_embedding).label(
            "distance"
        )
        statement = (
            select(LongTermMemoryRecord, distance)
            .where(LongTermMemoryRecord.namespace_key == namespace.key)
            .where(LongTermMemoryRecord.embedding.is_not(None))
            .order_by(distance)
            .limit(top_k)
        )
        if kind is not None:
            statement = statement.where(LongTermMemoryRecord.kind == kind.value)
        if metadata_filters:
            for key, value in metadata_filters.items():
                statement = statement.where(
                    LongTermMemoryRecord.memory_metadata[key].astext == str(value)
                )

        rows = (await self.session.execute(statement)).all()
        return [_record_to_memory(record) for record, _ in rows]


def _apply_memory_to_record(
    record: LongTermMemoryRecord,
    memory: MemoryRecord,
) -> None:
    record.namespace_scope = memory.namespace.scope.value
    record.namespace_path = list(memory.namespace.path)
    record.namespace_key = memory.namespace.key
    record.kind = memory.kind.value
    record.content = memory.content
    record.memory_metadata = memory.metadata
    record.embedding = memory.embedding
    record.source_session_id = memory.source_session_id
    record.source_user_id = memory.source_user_id
    record.quality_score = memory.quality_score


def _record_to_memory(record: LongTermMemoryRecord) -> MemoryRecord:
    return MemoryRecord(
        id=record.id,
        namespace=MemoryNamespace(
            scope=MemoryScope(record.namespace_scope),
            path=tuple(record.namespace_path),
        ),
        kind=MemoryKind(record.kind),
        content=record.content,
        metadata=record.memory_metadata,
        embedding=record.embedding,
        source_session_id=record.source_session_id,
        source_user_id=record.source_user_id,
        quality_score=record.quality_score,
        created_at=record.created_at,
    )
