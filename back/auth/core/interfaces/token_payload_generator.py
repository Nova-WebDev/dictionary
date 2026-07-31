from abc import ABC, abstractmethod

from auth.core.entities.token_payload import TokenPayload


class ITokenPayloadGenerator(ABC):
    @abstractmethod
    async def generate_payload(self, base: dict) -> TokenPayload: ...