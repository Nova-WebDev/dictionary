from user.core.entities.user_entity import UserEntity
from user.core.errors.errors import (
    EmailAlreadyExistsError,
    InvalidRoleError,
    PermissionDeniedError,
)
from user.core.interfaces.user_repository import IUserRepository


class CreateUserUC:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self, requester_role: int, email: str, role: int) -> UserEntity:
        if requester_role != 20:
            raise PermissionDeniedError()

        if role < 1 or role >= 20:
            raise InvalidRoleError()

        existing_user = await self.repo.get_by_email(email)
        if existing_user is not None:
            raise EmailAlreadyExistsError()

        return await self.repo.create_user(email=email, role=role)
