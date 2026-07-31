from typing import Protocol

from user.core.entities.user_entity import UserEntity


class IUserLookup(Protocol):
    async def get_by_public_id(self, public_id: str) -> UserEntity | None: ...