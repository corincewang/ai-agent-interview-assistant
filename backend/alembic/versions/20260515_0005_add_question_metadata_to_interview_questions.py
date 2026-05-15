"""add question_metadata to interview_questions

Revision ID: 20260515_0005
Revises: 20260515_0004
Create Date: 2026-05-15 17:30:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "20260515_0005"
down_revision: str | None = "20260515_0004"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "interview_questions",
        sa.Column(
            "question_metadata",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )
    op.execute(
        "UPDATE interview_questions SET question_metadata = '{}'::jsonb "
        "WHERE question_metadata IS NULL"
    )
    op.alter_column("interview_questions", "question_metadata", nullable=False)


def downgrade() -> None:
    op.drop_column("interview_questions", "question_metadata")
