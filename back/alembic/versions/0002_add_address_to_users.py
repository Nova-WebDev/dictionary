"""add address to users

Revision ID: 0002
Revises: 0001
Create Date: 2026-09-04

"""
from alembic import op
import sqlalchemy as sa

revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("address", sa.String(length=255), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("users", "address")
