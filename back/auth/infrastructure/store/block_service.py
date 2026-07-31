from redis.asyncio import Redis
from auth.core.interfaces.block_service import IBlockService


class BlockService(IBlockService):
    def __init__(self, redis: Redis):
        self.redis = redis

    @staticmethod
    def _key(email: str) -> str:
        return f"auth:block:{email}"

    async def is_blocked(self, email: str) -> bool:
        key = self._key(email)
        exists = await self.redis.exists(key)
        return exists == 1

    async def block(self, email: str, ttl):
        key = self._key(email)
        await self.redis.set(key, "1", ex=ttl)
