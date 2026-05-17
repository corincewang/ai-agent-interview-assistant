import hashlib
from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.domain.models import MemoryKind, MemoryNamespace, MemoryRecord, MemoryScope


class MemoryNamespaceFactory:
    def shared_role_intel(
        self,
        company_name: str,
        role_title: str,
        jd_text: str,
    ) -> MemoryNamespace:
        return MemoryNamespace(
            scope=MemoryScope.SHARED,
            path=("role_intel", _slug(company_name), _role_hash(role_title, jd_text)),
        )

    def shared_question_bank(
        self,
        target_track: str,
        company_name: str,
        role_title: str,
        jd_text: str,
    ) -> MemoryNamespace:
        return MemoryNamespace(
            scope=MemoryScope.SHARED,
            path=(
                "question_bank",
                _slug(target_track),
                _slug(company_name),
                _role_hash(role_title, jd_text),
            ),
        )

    def user_profile(self, user_id: UUID) -> MemoryNamespace:
        return MemoryNamespace(
            scope=MemoryScope.USER,
            path=(str(user_id), "profile"),
        )

    def user_question_history(self, user_id: UUID) -> MemoryNamespace:
        return MemoryNamespace(
            scope=MemoryScope.USER,
            path=(str(user_id), "question_history"),
        )

    def session_generated_questions(self, session_id: UUID) -> MemoryNamespace:
        return MemoryNamespace(
            scope=MemoryScope.SESSION,
            path=(str(session_id), "generated_questions"),
        )

    def session_summary(self, session_id: UUID) -> MemoryNamespace:
        return MemoryNamespace(
            scope=MemoryScope.SESSION,
            path=(str(session_id), "summary"),
        )


def build_memory_record(
    namespace: MemoryNamespace,
    kind: MemoryKind,
    content: dict,
    metadata: dict | None = None,
    embedding: list[float] | None = None,
    source_session_id: UUID | None = None,
    source_user_id: UUID | None = None,
    quality_score: float | None = None,
) -> MemoryRecord:
    return MemoryRecord(
        id=uuid4(),
        namespace=namespace,
        kind=kind,
        content=content,
        metadata=metadata or {},
        embedding=embedding,
        source_session_id=source_session_id,
        source_user_id=source_user_id,
        quality_score=quality_score,
        created_at=datetime.now(timezone.utc),
    )


def _role_hash(role_title: str, jd_text: str) -> str:
    normalized = f"{role_title.strip().lower()}\n{jd_text.strip().lower()}"
    return hashlib.sha256(normalized.encode("utf-8")).hexdigest()[:12]


def _slug(value: str) -> str:
    cleaned = value.strip().lower()
    chars: list[str] = []
    previous_dash = False

    for char in cleaned:
        if char.isalnum():
            chars.append(char)
            previous_dash = False
            continue

        if not previous_dash:
            chars.append("-")
            previous_dash = True

    return "".join(chars).strip("-") or "unknown"
