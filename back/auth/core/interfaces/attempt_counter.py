from abc import ABC, abstractmethod


class IAttemptCounter(ABC):
    @abstractmethod
    async def increment(self, email: str) -> int: ...