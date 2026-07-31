from abc import ABC, abstractmethod


class ITokenSigner(ABC):
    @abstractmethod
    async def sign(self, unsigned: str) -> bytes: ...