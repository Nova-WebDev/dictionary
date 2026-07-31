from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from auth.core.errors.errors import EmailBlockCheckError
from auth.core.interfaces.email_block_checker import IEmailBlockChecker
from user.infrastructure.data.models import User


class EmailBlockRepository(IEmailBlockChecker):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def is_blocked(self, email: str) -> bool:
        try:
            result = await self.session.execute(
                select(User.is_blocked).where(User.email == email)
            )
        except Exception as exc:
            raise EmailBlockCheckError() from exc

        value = result.scalar_one_or_none()

        if value is None:
            return False

        return value