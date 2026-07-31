from abc import ABC, abstractmethod


class IRefreshTokenStore(ABC):
    @abstractmethod
    async def get(self, token: str) -> dict | None: ...

    @abstractmethod
    async def save(self, token: str, user_data: dict) -> None: ...

    @abstractmethod
    async def delete(self, token: str) -> None: ...