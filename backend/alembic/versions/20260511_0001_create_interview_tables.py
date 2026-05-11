"""create interview assistant tables

Revision ID: 20260511_0001
Revises:
Create Date: 2026-05-11
"""

from collections.abc import Sequence

from alembic import op
import pgvector.sqlalchemy
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260511_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "interview_sessions",
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("company_name", sa.String(length=255), nullable=False),
        sa.Column("role_title", sa.String(length=255), nullable=False),
        sa.Column("jd_text", sa.Text(), nullable=False),
        sa.Column("mode", sa.String(length=50), nullable=False),
        sa.Column("status", sa.String(length=50), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_interview_sessions_user_id", "interview_sessions", ["user_id"])

    op.create_table(
        "documents",
        sa.Column("session_id", sa.Uuid(), nullable=False),
        sa.Column("document_type", sa.String(length=80), nullable=False),
        sa.Column("file_name", sa.String(length=500), nullable=False),
        sa.Column("file_path", sa.Text(), nullable=True),
        sa.Column("raw_text", sa.Text(), nullable=False),
        sa.Column("document_metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["interview_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_documents_document_type", "documents", ["document_type"])
    op.create_index("ix_documents_session_id", "documents", ["session_id"])

    op.create_table(
        "interview_plans",
        sa.Column("session_id", sa.Uuid(), nullable=False),
        sa.Column("mode", sa.String(length=50), nullable=False),
        sa.Column("candidate_storyline", sa.Text(), nullable=False),
        sa.Column("rubric", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("planned_deep_dives", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("plan_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["interview_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("session_id"),
    )
    op.create_index("ix_interview_plans_session_id", "interview_plans", ["session_id"], unique=True)

    op.create_table(
        "interview_turns",
        sa.Column("session_id", sa.Uuid(), nullable=False),
        sa.Column("role", sa.String(length=50), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("turn_metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["interview_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_interview_turns_session_id", "interview_turns", ["session_id"])

    op.create_table(
        "reports",
        sa.Column("session_id", sa.Uuid(), nullable=False),
        sa.Column("report", sa.Text(), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["session_id"], ["interview_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("session_id"),
    )
    op.create_index("ix_reports_session_id", "reports", ["session_id"], unique=True)

    op.create_table(
        "document_chunks",
        sa.Column("session_id", sa.Uuid(), nullable=False),
        sa.Column("document_id", sa.Uuid(), nullable=False),
        sa.Column("document_type", sa.String(length=80), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("start_char", sa.Integer(), nullable=True),
        sa.Column("end_char", sa.Integer(), nullable=True),
        sa.Column("embedding_model", sa.String(length=120), nullable=True),
        sa.Column("embedding", pgvector.sqlalchemy.Vector(dim=1536), nullable=True),
        sa.Column("chunk_metadata", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["document_id"], ["documents.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["session_id"], ["interview_sessions.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_document_chunks_document_id", "document_chunks", ["document_id"])
    op.create_index("ix_document_chunks_document_type", "document_chunks", ["document_type"])
    op.create_index("ix_document_chunks_session_id", "document_chunks", ["session_id"])

    op.create_table(
        "interview_questions",
        sa.Column("plan_id", sa.Uuid(), nullable=False),
        sa.Column("position", sa.Integer(), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("topic", sa.String(length=255), nullable=False),
        sa.Column("difficulty", sa.String(length=50), nullable=False),
        sa.Column("expected_signals", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("follow_up_strategy", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["plan_id"], ["interview_plans.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_interview_questions_plan_id", "interview_questions", ["plan_id"])

    op.create_table(
        "answer_evaluations",
        sa.Column("session_id", sa.Uuid(), nullable=False),
        sa.Column("turn_id", sa.Uuid(), nullable=True),
        sa.Column("question_id", sa.Uuid(), nullable=True),
        sa.Column("scores", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("strengths", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("weaknesses", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("improved_answer", sa.Text(), nullable=False),
        sa.Column("next_practice_steps", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["question_id"], ["interview_questions.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["session_id"], ["interview_sessions.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["turn_id"], ["interview_turns.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_answer_evaluations_question_id", "answer_evaluations", ["question_id"])
    op.create_index("ix_answer_evaluations_session_id", "answer_evaluations", ["session_id"])
    op.create_index("ix_answer_evaluations_turn_id", "answer_evaluations", ["turn_id"])


def downgrade() -> None:
    op.drop_index("ix_answer_evaluations_turn_id", table_name="answer_evaluations")
    op.drop_index("ix_answer_evaluations_session_id", table_name="answer_evaluations")
    op.drop_index("ix_answer_evaluations_question_id", table_name="answer_evaluations")
    op.drop_table("answer_evaluations")
    op.drop_index("ix_interview_questions_plan_id", table_name="interview_questions")
    op.drop_table("interview_questions")
    op.drop_index("ix_document_chunks_session_id", table_name="document_chunks")
    op.drop_index("ix_document_chunks_document_type", table_name="document_chunks")
    op.drop_index("ix_document_chunks_document_id", table_name="document_chunks")
    op.drop_table("document_chunks")
    op.drop_index("ix_reports_session_id", table_name="reports")
    op.drop_table("reports")
    op.drop_index("ix_interview_turns_session_id", table_name="interview_turns")
    op.drop_table("interview_turns")
    op.drop_index("ix_interview_plans_session_id", table_name="interview_plans")
    op.drop_table("interview_plans")
    op.drop_index("ix_documents_session_id", table_name="documents")
    op.drop_index("ix_documents_document_type", table_name="documents")
    op.drop_table("documents")
    op.drop_index("ix_interview_sessions_user_id", table_name="interview_sessions")
    op.drop_table("interview_sessions")
