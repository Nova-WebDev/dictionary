import uuid

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from auth.core.entities.user_identity import UserIdentity
from auth.core.errors.errors import UserCreationError
from auth.core.interfaces.user_service import IUserService
from user.infrastructure.data.models import User


class UserRepository(IUserService):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, email: str) -> UserIdentity:
        user = await self._get_by_email(email)
        if user is not None:
            return UserIdentity(
                email=user.email,
                role=user.role,
                public_id=user.public_id,
            )

        public_id = uuid.uuid4().hex

        try:
            new_user = User(
                email=email,
                public_id=public_id,
                role=1,
                is_blocked=False,
            )
            self.session.add(new_user)
            await self.session.flush()
        except IntegrityError:
            await self.session.rollback()
            user = await self._get_by_email(email)
            if user is None:
                raise UserCreationError()
            return UserIdentity(
                email=user.email,
                role=user.role,
                public_id=user.public_id,
            )

        return UserIdentity(
            email=email,
            role=1,
            public_id=public_id,
        )

    async def _get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()