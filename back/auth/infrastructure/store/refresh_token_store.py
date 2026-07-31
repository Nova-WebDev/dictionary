import json

from redis.asyncio import Redis

from app.settings import settings
from auth.core.interfaces.refresh_token_store import IRefreshTokenStore
from auth.core.errors.errors import RefreshTokenPersistenceError


class RefreshTokenStore(IRefreshTokenStore):
    def __init__(self, redis: Redis):
        self.redis = redis
        self.ttl = settings.refresh_token_ttl_seconds

    @staticmethod
    def _key(token: str) -> str:
        return f"auth:refresh:{token}"

    async def get(self, token: str) -> dict | None:
        key = self._key(token)
        try:
            data = await self.redis.get(key)
        except Exception as exc:
            raise RefreshTokenPersistenceError() from exc

        if not data:
            return None
        return json.loads(data)

    async def save(self, token: str, user_data: dict) -> None:
        key = self._key(token)
        try:
            await self.redis.set(key, json.dumps(user_data), ex=self.ttl)
        except Exception as exc:
            raise RefreshTokenPersistenceError() from exc

    async def delete(self, token: str) -> None:
        key = self._key(token)
        try:
            await self.redis.delete(key)
        except Exception as exc:
            raise RefreshTokenPersistenceError() from exc