from abc import ABC, abstractmethod

from auth.core.entities.user_identity import UserIdentity


class IUserService(ABC):
    @abstractmethod
    async def create_user(self, email: str) -> UserIdentity: ...