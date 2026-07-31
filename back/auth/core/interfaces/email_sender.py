from abc import ABC, abstractmethod


class IEmailSender(ABC):
    @abstractmethod
    async def send(self, email: str, code: str) -> None: ...