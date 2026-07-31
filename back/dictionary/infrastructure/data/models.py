import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.data.base import Base


class WordEntry(Base):
    __tablename__ = "words"

    public_id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )

    english_word: Mapped[str] = mapped_column(String(255))

    persian_word: Mapped[str] = mapped_column(String(255))

    author_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.public_id", ondelete="CASCADE")
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    __table_args__ = (
        Index(
            "idx_english_word_trgm",
            "english_word",
            postgresql_using="gin",
            postgresql_ops={"english_word": "gin_trgm_ops"},
        ),
        Index(
            "idx_persian_word_trgm",
            "persian_word",
            postgresql_using="gin",
            postgresql_ops={"persian_word": "gin_trgm_ops"},
        ),
    )