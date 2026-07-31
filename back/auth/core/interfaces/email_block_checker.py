from abc import ABC, abstractmethod


class IEmailBlockChecker(ABC):
    @abstractmethod
    async def is_blocked(self, email: str) -> bool: ...