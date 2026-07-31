from abc import ABC, abstractmethod


class IBlockService(ABC):
    @abstractmethod
    async def is_blocked(self, email: str) -> bool: ...

    @abstractmethod
    async def block(self, email: str, ttl: int) -> None: ...