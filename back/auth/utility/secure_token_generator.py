import secrets

from auth.core.interfaces.token_generator import ITokenGenerator


class SecureTokenGenerator(ITokenGenerator):
    def __init__(self, length: int = 32):
        self.length = length

    async def generate(self) -> str:
        return secrets.token_urlsafe(self.length)