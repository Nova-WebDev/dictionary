from typing import Optional
from redis.asyncio import Redis

from auth.core.interfaces.code_store import ICodeStore


class CodeStore(ICodeStore):
    def __init__(self, redis: Redis, ttl_seconds: int = 120):
        self.redis = redis
        self.ttl = ttl_seconds

    @staticmethod
    def _key(email: str) -> str:
        return f"auth:code:{email}"

    async def get(self, email: str) -> Optional[str]:
        key = self._key(email)
        return await self.redis.get(key)

    async def save(self, email: str, code: str):
        key = self._key(email)
        await self.redis.set(key, code, ex=self.ttl)

    async def delete(self, email: str):
        key = self._key(email)
        await self.redis.delete(key)
