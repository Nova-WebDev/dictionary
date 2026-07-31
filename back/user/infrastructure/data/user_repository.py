from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from user.core.entities.user_entity import UserEntity
from user.core.entities.user_order_field import UserOrderField
from user.core.errors.errors import UserNotFoundError, UsernameUpdateError
from user.core.interfaces.user_repository import IUserRepository
from user.infrastructure.data.models import User


class UserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    @staticmethod
    def _to_entity(user: User) -> UserEntity:
        return UserEntity(
            public_id=user.public_id,
            email=user.email,
            username=user.username,
            role=user.role,
            is_blocked=user.is_blocked,
            created_at=user.created_at,
        )

    async def get_by_public_id(self, public_id: str) -> UserEntity | None:
        result = await self.session.execute(
            select(User).where(User.public_id == public_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            return None

        return self._to_entity(user)

    async def update_block_status(self, public_id: str, is_blocked: bool) -> UserEntity:
        result = await self.session.execute(
            select(User).where(User.public_id == public_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            raise UserNotFoundError()

        user.is_blocked = is_blocked
        await self.session.flush()

        return self._to_entity(user)

    async def update_role(self, public_id: str, new_role: int) -> UserEntity:
        result = await self.session.execute(
            select(User).where(User.public_id == public_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            raise UserNotFoundError()

        user.role = new_role
        await self.session.flush()

        return self._to_entity(user)

    async def update_username(self, public_id: str, username: str) -> UserEntity:
        result = await self.session.execute(
            select(User).where(User.public_id == public_id)
        )
        user = result.scalar_one_or_none()

        if user is None:
            raise UserNotFoundError()

        try:
            user.username = username
            await self.session.flush()
        except Exception as exc:
            raise UsernameUpdateError() from exc

        return self._to_entity(user)

    async def get_users_paginated(
        self,
        offset: int,
        limit: int,
        search: str,
        exclude_public_id: str | None,
        order_by: UserOrderField,
        descending: bool,
    ) -> list[UserEntity]:
        stmt = select(User)

        if search:
            stmt = stmt.where(User.username.ilike(f"%{search}%"))

        if exclude_public_id is not None:
            stmt = stmt.where(User.public_id != exclude_public_id)

        order_column = getattr(User, order_by)
        stmt = stmt.order_by(order_column.desc() if descending else order_column.asc())

        stmt = stmt.offset(offset).limit(limit)

        result = await self.session.execute(stmt)
        users = result.scalars().all()

        return [self._to_entity(user) for user in users]

    async def count_users(self, search: str, exclude_public_id: str | None) -> int:
        stmt = select(func.count()).select_from(User)

        if search:
            stmt = stmt.where(User.username.ilike(f"%{search}%"))

        if exclude_public_id is not None:
            stmt = stmt.where(User.public_id != exclude_public_id)

        result = await self.session.execute(stmt)
        return result.scalar_one()