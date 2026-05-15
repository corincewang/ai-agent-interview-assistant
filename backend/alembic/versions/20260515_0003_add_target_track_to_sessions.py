"""add target_track to interview_sessions

Revision ID: 20260515_0003
Revises: 20260511_0002
Create Date: 2026-05-15 15:50:00
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "20260515_0003"
down_revision: str | None = "20260511_0002"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "interview_sessions",
        sa.Column("target_track", sa.String(length=255), nullable=True),
    )
    op.execute("UPDATE interview_sessions SET target_track = role_title")
    op.alter_column("interview_sessions", "target_track", nullable=False)


def downgrade() -> None:
    op.drop_column("interview_sessions", "target_track")
