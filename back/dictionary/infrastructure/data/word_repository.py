from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from dictionary.core.entities.word_entry import WordEntryEntity
from dictionary.core.entities.word_entry_with_author import WordEntryWithAuthorEntity
from dictionary.core.entities.word_order_field import WordOrderField
from dictionary.core.errors.errors import WordNotFoundError, WordPersistenceError
from dictionary.core.interfaces.word_repository import IWordRepository
from dictionary.infrastructure.data.models import WordEntry
from user.infrastructure.data.models import User


class WordRepository(IWordRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _to_entity(word: WordEntry) -> WordEntryEntity:
        return WordEntryEntity(
            public_id=word.public_id,
            persian_word=word.persian_word,
            english_word=word.english_word,
            author_id=word.author_id,
            created_at=word.created_at,
        )

    async def get_by_id(self, public_id: str) -> WordEntryEntity | None:
        result = await self.session.execute(
            select(WordEntry).where(WordEntry.public_id == public_id)
        )
        word = result.scalar_one_or_none()

        if word is None:
            return None

        return self._to_entity(word)

    async def create(
        self, persian_word: str, english_word: str, author_id: str
    ) -> WordEntryEntity:
        word = WordEntry(
            persian_word=persian_word,
            english_word=english_word,
            author_id=author_id,
        )

        try:
            self.session.add(word)
            await self.session.flush()
        except Exception as exc:
            raise WordPersistenceError() from exc

        return self._to_entity(word)

    async def update(
        self, public_id: str, persian_word: str, english_word: str
    ) -> WordEntryEntity:
        result = await self.session.execute(
            select(WordEntry).where(WordEntry.public_id == public_id)
        )
        word = result.scalar_one_or_none()

        if word is None:
            raise WordNotFoundError()

        try:
            word.persian_word = persian_word
            word.english_word = english_word
            await self.session.flush()
        except Exception as exc:
            raise WordPersistenceError() from exc

        return self._to_entity(word)

    async def delete(self, public_id: str) -> None:
        result = await self.session.execute(
            select(WordEntry).where(WordEntry.public_id == public_id)
        )
        word = result.scalar_one_or_none()

        if word is None:
            raise WordNotFoundError()

        try:
            await self.session.delete(word)
            await self.session.flush()
        except Exception as exc:
            raise WordPersistenceError() from exc

    async def search_by_persian(self, query: str) -> list[WordEntryEntity]:
        result = await self.session.execute(
            select(WordEntry).where(WordEntry.persian_word.ilike(f"%{query}%"))
        )
        words = result.scalars().all()
        return [self._to_entity(word) for word in words]

    async def search_by_english(self, query: str) -> list[WordEntryEntity]:
        result = await self.session.execute(
            select(WordEntry).where(WordEntry.english_word.ilike(f"%{query}%"))
        )
        words = result.scalars().all()
        return [self._to_entity(word) for word in words]

    async def get_paginated_with_author(
        self,
        offset: int,
        limit: int,
        search: str,
        order_by: WordOrderField,
        descending: bool,
    ) -> list[WordEntryWithAuthorEntity]:
        stmt = select(
            WordEntry.public_id,
            WordEntry.persian_word,
            WordEntry.english_word,
            WordEntry.created_at,
            User.username,
        ).outerjoin(User, WordEntry.author_id == User.public_id)

        if search:
            stmt = stmt.where(
                or_(
                    WordEntry.persian_word.ilike(f"%{search}%"),
                    WordEntry.english_word.ilike(f"%{search}%"),
                )
            )

        order_column = getattr(WordEntry, order_by)
        stmt = stmt.order_by(order_column.desc() if descending else order_column.asc())

        stmt = stmt.offset(offset).limit(limit)

        result = await self.session.execute(stmt)
        rows = result.all()

        return [
            WordEntryWithAuthorEntity(
                public_id=row.public_id,
                persian_word=row.persian_word,
                english_word=row.english_word,
                author_name=row.username,
                created_at=row.created_at,
            )
            for row in rows
        ]

    async def count(self, search: str) -> int:
        stmt = select(func.count()).select_from(WordEntry)

        if search:
            stmt = stmt.where(
                or_(
                    WordEntry.persian_word.ilike(f"%{search}%"),
                    WordEntry.english_word.ilike(f"%{search}%"),
                )
            )

        result = await self.session.execute(stmt)
        return result.scalar_one()