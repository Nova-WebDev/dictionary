from user.core.entities.user_entity import UserEntity
from user.core.errors.errors import UserNotFoundError
from user.core.interfaces.user_repository import IUserRepository


class GetUserProfileByPublicIdUC:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self, public_id: str) -> UserEntity:
        user = await self.repo.get_by_public_id(public_id)
        if user is None:
            raise UserNotFoundError()
        return user