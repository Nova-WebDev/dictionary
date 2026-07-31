from dictionary.core.errors.errors import PermissionDeniedError, WordNotFoundError
from dictionary.core.interfaces.user_lookup import IUserLookup
from dictionary.core.interfaces.word_repository import IWordRepository


class DeleteWordEntryUC:
    def __init__(
        self,
        repo: IWordRepository,
        user_lookup: IUserLookup,
        min_role_when_author_unknown: int = 10,
    ):
        self.repo = repo
        self.user_lookup = user_lookup
        self.min_role_when_author_unknown = min_role_when_author_unknown

    async def execute(self, requester_role: int, public_id: str) -> None:
        word = await self.repo.get_by_id(public_id)
        if word is None:
            raise WordNotFoundError()

        if word.author_id is None:
            if requester_role < self.min_role_when_author_unknown:
                raise PermissionDeniedError()
        else:
            author = await self.user_lookup.get_by_public_id(word.author_id)
            author_role = author.role if author is not None else self.min_role_when_author_unknown

            if requester_role < author_role:
                raise PermissionDeniedError()

        await self.repo.delete(public_id)