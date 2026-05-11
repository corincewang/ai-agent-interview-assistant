"""add interview plan critiques

Revision ID: 20260511_0002
Revises: 20260511_0001
Create Date: 2026-05-11
"""

from collections.abc import Sequence

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision: str = "20260511_0002"
down_revision: str | None = "20260511_0001"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "interview_plan_critiques",
        sa.Column("session_id", sa.Uuid(), nullable=False),
        sa.Column("plan_id", sa.Uuid(), nullable=True),
        sa.Column("overall_score", sa.Float(), nullable=False),
        sa.Column("quality_gate_passed", sa.Boolean(), nullable=False),
        sa.Column("coverage_summary", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "revision_recommendations",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("critique_payload", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["plan_id"], ["interview_plans.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["interview_sessions.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("plan_id"),
        sa.UniqueConstraint("session_id"),
    )
    op.create_index(
        "ix_interview_plan_critiques_plan_id",
        "interview_plan_critiques",
        ["plan_id"],
        unique=True,
    )
    op.create_index(
        "ix_interview_plan_critiques_session_id",
        "interview_plan_critiques",
        ["session_id"],
        unique=True,
    )

    op.create_table(
        "question_critiques",
        sa.Column("plan_critique_id", sa.Uuid(), nullable=False),
        sa.Column("question_id", sa.Uuid(), nullable=True),
        sa.Column("resume_grounding_score", sa.Float(), nullable=False),
        sa.Column("jd_coverage_score", sa.Float(), nullable=False),
        sa.Column("rag_grounding_score", sa.Float(), nullable=False),
        sa.Column("specificity_score", sa.Float(), nullable=False),
        sa.Column("follow_up_potential_score", sa.Float(), nullable=False),
        sa.Column("overall_score", sa.Float(), nullable=False),
        sa.Column("strengths", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "improvement_suggestions",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["plan_critique_id"],
            ["interview_plan_critiques.id"],
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["question_id"],
            ["interview_questions.id"],
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_question_critiques_plan_critique_id",
        "question_critiques",
        ["plan_critique_id"],
    )
    op.create_index("ix_question_critiques_question_id", "question_critiques", ["question_id"])


def downgrade() -> None:
    op.drop_index("ix_question_critiques_question_id", table_name="question_critiques")
    op.drop_index(
        "ix_question_critiques_plan_critique_id",
        table_name="question_critiques",
    )
    op.drop_table("question_critiques")
    op.drop_index(
        "ix_interview_plan_critiques_session_id",
        table_name="interview_plan_critiques",
    )
    op.drop_index(
        "ix_interview_plan_critiques_plan_id",
        table_name="interview_plan_critiques",
    )
    op.drop_table("interview_plan_critiques")
