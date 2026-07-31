from redis.asyncio import Redis

from app.settings import settings
from auth.core.interfaces.user_remove_store import IUserRemoveStore
from auth.core.errors.errors import UserStatePersistenceError


class UserRemoveStore(IUserRemoveStore):
    def __init__(self, redis: Redis):
        self.redis = redis
        self.ttl = settings.refresh_token_ttl_seconds

    @staticmethod
    def _key(public_id: str) -> str:
        return f"auth:user_remove:{public_id}"

    async def block(self, public_id: str) -> None:
        key = self._key(public_id)
        try:
            await self.redis.set(key, 1, ex=self.ttl)
        except Exception as exc:
            raise UserStatePersistenceError() from exc

    async def unblock(self, public_id: str) -> None:
        key = self._key(public_id)
        try:
            await self.redis.delete(key)
        except Exception as exc:
            raise UserStatePersistenceError() from exc

    async def is_blocked(self, public_id: str) -> bool:
        key = self._key(public_id)
        try:
            exists = await self.redis.exists(key)
        except Exception as exc:
            raise UserStatePersistenceError() from exc
        return exists == 1