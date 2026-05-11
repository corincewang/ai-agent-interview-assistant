from typing import Any
from uuid import UUID

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base, TimestampMixin, UUIDPrimaryKeyMixin


EMBEDDING_DIMENSIONS = 1536


class InterviewSessionRecord(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "interview_sessions"

    user_id: Mapped[UUID] = mapped_column(Uuid(as_uuid=True), nullable=False, index=True)
    company_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role_title: Mapped[str] = mapped_column(String(255), nullable=False)
    jd_text: Mapped[str] = mapped_column(Text, nullable=False)
    mode: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="created")

    documents: Mapped[list["DocumentRecord"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
    interview_plan: Mapped["InterviewPlanRecord | None"] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
    turns: Mapped[list["InterviewTurnRecord"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
    evaluations: Mapped[list["AnswerEvaluationRecord"]] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )
    report: Mapped["ReportRecord | None"] = relationship(
        back_populates="session",
        cascade="all, delete-orphan",
    )


class DocumentRecord(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "documents"

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    document_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    file_name: Mapped[str] = mapped_column(String(500), nullable=False)
    file_path: Mapped[str | None] = mapped_column(Text)
    raw_text: Mapped[str] = mapped_column(Text, nullable=False)
    document_metadata: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)

    session: Mapped[InterviewSessionRecord] = relationship(back_populates="documents")
    chunks: Mapped[list["DocumentChunkRecord"]] = relationship(
        back_populates="document",
        cascade="all, delete-orphan",
    )


class DocumentChunkRecord(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "document_chunks"

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    document_id: Mapped[UUID] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    document_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    start_char: Mapped[int | None] = mapped_column(Integer)
    end_char: Mapped[int | None] = mapped_column(Integer)
    embedding_model: Mapped[str | None] = mapped_column(String(120))
    embedding: Mapped[list[float] | None] = mapped_column(Vector(EMBEDDING_DIMENSIONS))
    chunk_metadata: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)

    document: Mapped[DocumentRecord] = relationship(back_populates="chunks")


class InterviewPlanRecord(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "interview_plans"

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    mode: Mapped[str] = mapped_column(String(50), nullable=False)
    candidate_storyline: Mapped[str] = mapped_column(Text, nullable=False)
    rubric: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    planned_deep_dives: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    plan_payload: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)

    session: Mapped[InterviewSessionRecord] = relationship(back_populates="interview_plan")
    questions: Mapped[list["InterviewQuestionRecord"]] = relationship(
        back_populates="plan",
        cascade="all, delete-orphan",
        order_by="InterviewQuestionRecord.position",
    )


class InterviewQuestionRecord(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "interview_questions"

    plan_id: Mapped[UUID] = mapped_column(
        ForeignKey("interview_plans.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    topic: Mapped[str] = mapped_column(String(255), nullable=False)
    difficulty: Mapped[str] = mapped_column(String(50), nullable=False)
    expected_signals: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    follow_up_strategy: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)

    plan: Mapped[InterviewPlanRecord] = relationship(back_populates="questions")


class InterviewTurnRecord(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "interview_turns"

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    role: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    turn_metadata: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)

    session: Mapped[InterviewSessionRecord] = relationship(back_populates="turns")


class AnswerEvaluationRecord(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "answer_evaluations"

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    turn_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("interview_turns.id", ondelete="SET NULL"),
        index=True,
    )
    question_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("interview_questions.id", ondelete="SET NULL"),
        index=True,
    )
    scores: Mapped[dict[str, Any]] = mapped_column(JSONB, nullable=False, default=dict)
    strengths: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    weaknesses: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)
    improved_answer: Mapped[str] = mapped_column(Text, nullable=False)
    next_practice_steps: Mapped[list[str]] = mapped_column(JSONB, nullable=False, default=list)

    session: Mapped[InterviewSessionRecord] = relationship(back_populates="evaluations")


class ReportRecord(Base, UUIDPrimaryKeyMixin, TimestampMixin):
    __tablename__ = "reports"

    session_id: Mapped[UUID] = mapped_column(
        ForeignKey("interview_sessions.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
        index=True,
    )
    report: Mapped[str] = mapped_column(Text, nullable=False)

    session: Mapped[InterviewSessionRecord] = relationship(back_populates="report")
