from dictionary.core.entities.word_entry import WordEntryEntity
from dictionary.core.errors.errors import PermissionDeniedError
from dictionary.core.interfaces.word_repository import IWordRepository


class CreateWordEntryUC:
    def __init__(self, repo: IWordRepository, min_create_role: int = 10):
        self.repo = repo
        self.min_create_role = min_create_role

    async def execute(
        self,
        requester_role: int,
        author_id: str,
        persian_word: str,
        english_word: str,
    ) -> WordEntryEntity:
        if requester_role < self.min_create_role:
            raise PermissionDeniedError()

        return await self.repo.create(
            persian_word=persian_word,
            english_word=english_word,
            author_id=author_id,
        )