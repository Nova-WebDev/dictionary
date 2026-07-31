from dataclasses import asdict

from auth.core.entities.user_identity import UserIdentity
from auth.core.entities.refresh_token import RefreshToken
from auth.core.errors.errors import RefreshTokenPersistenceError
from auth.core.interfaces.token_generator import ITokenGenerator
from auth.core.interfaces.refresh_token_store import IRefreshTokenStore


class GenerateRefreshToken:
    def __init__(self, generator: ITokenGenerator, store: IRefreshTokenStore):
        self.generator = generator
        self.store = store

    async def execute(self, user: UserIdentity) -> RefreshToken:
        token = await self.generator.generate()

        try:
            await self.store.save(token, asdict(user))
        except Exception as exc:
            raise RefreshTokenPersistenceError() from exc

        return RefreshToken(
            token=token,
            public_id=user.public_id,
            role=user.role,
            email=user.email,
        )