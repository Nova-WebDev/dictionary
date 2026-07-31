from redis.asyncio import Redis
from auth.core.interfaces.attempt_counter import IAttemptCounter


class AttemptCounter(IAttemptCounter):
    def __init__(self, redis: Redis, ttl_seconds: int = 300):
        self.redis = redis
        self.ttl = ttl_seconds

    @staticmethod
    def _key(email: str) -> str:
        return f"auth:attempts:{email}"

    async def increment(self, email: str) -> int:
        key = self._key(email)
        new_value = await self.redis.incr(key)
        if new_value == 1:
            await self.redis.expire(key, self.ttl)

        return new_value
