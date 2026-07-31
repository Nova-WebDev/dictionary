from dictionary.core.entities.word_entry import WordEntryEntity
from dictionary.core.interfaces.word_repository import IWordRepository


class SearchEnglishToPersianUC:
    def __init__(self, repo: IWordRepository):
        self.repo = repo

    async def execute(self, query: str) -> list[WordEntryEntity]:
        return await self.repo.search_by_english(query)