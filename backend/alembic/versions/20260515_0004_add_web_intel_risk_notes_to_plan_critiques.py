"""add web_intel_risk_notes to interview_plan_critiques

Revision ID: 20260515_0004
Revises: 20260515_0003
Create Date: 2026-05-15 17:10:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "20260515_0004"
down_revision: str | None = "20260515_0003"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "interview_plan_critiques",
        sa.Column(
            "web_intel_risk_notes",
            postgresql.JSONB(astext_type=sa.Text()),
            nullable=True,
        ),
    )
    op.execute(
        "UPDATE interview_plan_critiques SET web_intel_risk_notes = '[]'::jsonb "
        "WHERE web_intel_risk_notes IS NULL"
    )
    op.alter_column("interview_plan_critiques", "web_intel_risk_notes", nullable=False)


def downgrade() -> None:
    op.drop_column("interview_plan_critiques", "web_intel_risk_notes")
