from redis.asyncio import Redis

from app.settings import settings
from auth.core.interfaces.user_role_store import IUserRoleStore
from auth.core.errors.errors import UserStatePersistenceError


class UserRoleStore(IUserRoleStore):
    def __init__(self, redis: Redis):
        self.redis = redis
        self.ttl = settings.refresh_token_ttl_seconds

    @staticmethod
    def _key(public_id: str) -> str:
        return f"auth:user_role:{public_id}"

    async def set_role(self, public_id: str, role: int) -> None:
        key = self._key(public_id)
        try:
            await self.redis.set(key, role, ex=self.ttl)
        except Exception as exc:
            raise UserStatePersistenceError() from exc

    async def get_role(self, public_id: str) -> int | None:
        key = self._key(public_id)
        try:
            data = await self.redis.get(key)
        except Exception as exc:
            raise UserStatePersistenceError() from exc

        if data is None:
            return None
        return int(data)