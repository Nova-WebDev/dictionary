from abc import ABC, abstractmethod

from user.core.entities.user_entity import UserEntity
from user.core.entities.user_order_field import UserOrderField

class IUserRepository(ABC):
    @abstractmethod
    async def get_by_public_id(self, public_id: str) -> UserEntity | None: ...

    @abstractmethod
    async def update_block_status(self, public_id: str, is_blocked: bool) -> UserEntity: ...

    @abstractmethod
    async def update_role(self, public_id: str, new_role: int) -> UserEntity: ...

    @abstractmethod
    async def update_username(self, public_id: str, username: str) -> UserEntity: ...

    @abstractmethod
    async def get_users_paginated(
        self,
        offset: int,
        limit: int,
        search: str,
        exclude_public_id: str | None,
        order_by: UserOrderField,
        descending: bool,
    ) -> list[UserEntity]: ...

    @abstractmethod
    async def count_users(self, search: str, exclude_public_id: str | None) -> int: ...