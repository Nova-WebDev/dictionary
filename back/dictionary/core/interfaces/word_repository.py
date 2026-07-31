from abc import ABC, abstractmethod

from dictionary.core.entities.word_entry import WordEntryEntity
from dictionary.core.entities.word_entry_with_author import WordEntryWithAuthorEntity
from dictionary.core.entities.word_order_field import WordOrderField


class IWordRepository(ABC):
    @abstractmethod
    async def get_by_id(self, public_id: str) -> WordEntryEntity | None: ...

    @abstractmethod
    async def create(
        self, persian_word: str, english_word: str, author_id: str
    ) -> WordEntryEntity: ...

    @abstractmethod
    async def update(
        self, public_id: str, persian_word: str, english_word: str
    ) -> WordEntryEntity: ...

    @abstractmethod
    async def delete(self, public_id: str) -> None: ...

    @abstractmethod
    async def search_by_persian(self, query: str) -> list[WordEntryEntity]: ...

    @abstractmethod
    async def search_by_english(self, query: str) -> list[WordEntryEntity]: ...

    @abstractmethod
    async def get_paginated_with_author(
        self,
        offset: int,
        limit: int,
        search: str,
        order_by: WordOrderField,
        descending: bool,
    ) -> list[WordEntryWithAuthorEntity]: ...

    @abstractmethod
    async def count(self, search: str) -> int: ...