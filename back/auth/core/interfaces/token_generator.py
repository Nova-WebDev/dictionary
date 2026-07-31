from abc import ABC, abstractmethod


class ITokenGenerator(ABC):
    @abstractmethod
    async def generate(self) -> str: ...