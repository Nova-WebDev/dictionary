from abc import ABC, abstractmethod


class ICodeGenerator(ABC):
    @abstractmethod
    async def generate(self) -> str: ...