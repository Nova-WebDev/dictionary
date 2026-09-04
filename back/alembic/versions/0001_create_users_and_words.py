"""create users and words tables

Revision ID: 0001
Revises:
Create Date: 2026-09-04

"""
from alembic import op
import sqlalchemy as sa

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("public_id", sa.String(length=36), primary_key=True),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("username", sa.String(length=50), nullable=True),
        sa.Column("role", sa.Integer(), nullable=True),
        sa.Column("is_blocked", sa.Boolean(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_index(
        op.f("ix_users_email"),
        "users",
        ["email"],
        unique=True,
    )
    op.create_index(
        "idx_username_trgm",
        "users",
        ["username"],
        unique=False,
        postgresql_using="gin",
        postgresql_ops={"username": "gin_trgm_ops"},
    )

    op.create_table(
        "words",
        sa.Column("public_id", sa.String(length=36), primary_key=True),
        sa.Column("english_word", sa.String(length=255), nullable=False),
        sa.Column("persian_word", sa.String(length=255), nullable=False),
        sa.Column(
            "author_id",
            sa.String(length=36),
            sa.ForeignKey("users.public_id", ondelete="CASCADE"),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )
    op.create_index(
        "idx_english_word_trgm",
        "words",
        ["english_word"],
        unique=False,
        postgresql_using="gin",
        postgresql_ops={"english_word": "gin_trgm_ops"},
    )
    op.create_index(
        "idx_persian_word_trgm",
        "words",
        ["persian_word"],
        unique=False,
        postgresql_using="gin",
        postgresql_ops={"persian_word": "gin_trgm_ops"},
    )


def downgrade() -> None:
    op.drop_table("words")
    op.drop_table("users")
