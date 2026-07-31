from abc import ABC, abstractmethod


class ICodeStore(ABC):
    @abstractmethod
    async def get(self, email: str) -> str | None: ...

    @abstractmethod
    async def save(self, email: str, code: str) -> None: ...

    @abstractmethod
    async def delete(self, email: str) -> None: ...