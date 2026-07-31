from abc import ABC, abstractmethod


class IUserRemoveStore(ABC):
    @abstractmethod
    async def block(self, public_id: str) -> None: ...

    @abstractmethod
    async def unblock(self, public_id: str) -> None: ...

    @abstractmethod
    async def is_blocked(self, public_id: str) -> bool: ...