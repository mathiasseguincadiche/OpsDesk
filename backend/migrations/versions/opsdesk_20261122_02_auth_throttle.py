"""Limitation des connexions stockée en base commune.

Revision ID: opsdesk_20261122_02
Revises: opsdesk_20261122_01
"""
from alembic import op
import sqlalchemy as sa

revision = "opsdesk_20261122_02"
down_revision = "opsdesk_20261122_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "login_throttle",
        sa.Column("key", sa.String(64), primary_key=True),
        sa.Column("attempt_count", sa.Integer(), nullable=False),
        sa.Column("window_started_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("blocked_until", sa.DateTime(timezone=True), nullable=True),
    )
    op.create_index("ix_login_throttle_window_started_at", "login_throttle", ["window_started_at"])


def downgrade() -> None:
    # Ne supprime aucune donnée métier ; l'opérateur doit retirer le code utilisateur d'abord.
    op.drop_index("ix_login_throttle_window_started_at", table_name="login_throttle")
    op.drop_table("login_throttle")
