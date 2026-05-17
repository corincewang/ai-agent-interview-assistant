"""add long term memories

Revision ID: 20260517_0006
Revises: 20260515_0005
Create Date: 2026-05-17 15:10:00
"""

from collections.abc import Sequence

import pgvector.sqlalchemy
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


revision: str = "20260517_0006"
down_revision: str | None = "20260515_0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "long_term_memories",
        sa.Column("namespace_scope", sa.String(length=50), nullable=False),
        sa.Column(
            "namespace_path",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("namespace_key", sa.String(length=500), nullable=False),
        sa.Column("kind", sa.String(length=80), nullable=False),
        sa.Column("content", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column(
            "memory_metadata",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=False,
        ),
        sa.Column("embedding", pgvector.sqlalchemy.Vector(dim=1536), nullable=True),
        sa.Column("source_session_id", sa.Uuid(), nullable=True),
        sa.Column("source_user_id", sa.Uuid(), nullable=True),
        sa.Column("quality_score", sa.Float(), nullable=True),
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
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_long_term_memories_namespace_scope",
        "long_term_memories",
        ["namespace_scope"],
    )
    op.create_index(
        "ix_long_term_memories_namespace_key",
        "long_term_memories",
        ["namespace_key"],
    )
    op.create_index("ix_long_term_memories_kind", "long_term_memories", ["kind"])
    op.create_index(
        "ix_long_term_memories_source_session_id",
        "long_term_memories",
        ["source_session_id"],
    )
    op.create_index(
        "ix_long_term_memories_source_user_id",
        "long_term_memories",
        ["source_user_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_long_term_memories_source_user_id", table_name="long_term_memories")
    op.drop_index(
        "ix_long_term_memories_source_session_id",
        table_name="long_term_memories",
    )
    op.drop_index("ix_long_term_memories_kind", table_name="long_term_memories")
    op.drop_index("ix_long_term_memories_namespace_key", table_name="long_term_memories")
    op.drop_index(
        "ix_long_term_memories_namespace_scope",
        table_name="long_term_memories",
    )
    op.drop_table("long_term_memories")
