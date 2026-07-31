from dictionary.core.entities.word_entry_with_author import WordEntryWithAuthorEntity
from dictionary.core.entities.word_order_field import WordOrderField
from dictionary.core.interfaces.word_repository import IWordRepository


class GetWordsPaginatedUC:
    def __init__(self, repo: IWordRepository):
        self.repo = repo

    async def execute(
        self,
        page: int,
        limit: int,
        search: str,
        order_by: WordOrderField,
        descending: bool,
    ) -> dict:
        if page < 1 or limit < 1:
            return {"words": [], "total_count": 0}

        offset = (page - 1) * limit

        total_count = await self.repo.count(search=search)
        words = await self.repo.get_paginated_with_author(
            offset=offset,
            limit=limit,
            search=search,
            order_by=order_by,
            descending=descending,
        )

        return {"words": words, "total_count": total_count}