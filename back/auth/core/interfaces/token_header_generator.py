from abc import ABC, abstractmethod

from auth.core.entities.token_header import TokenHeader


class ITokenHeaderGenerator(ABC):
    @abstractmethod
    async def generate_header(self) -> TokenHeader: ...