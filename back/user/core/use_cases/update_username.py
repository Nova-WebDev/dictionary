from user.core.entities.user_entity import UserEntity
from user.core.errors.errors import UsernameUpdateError, UserNotFoundError
from user.core.interfaces.user_repository import IUserRepository


class UpdateUsernameUC:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(self, public_id: str, username: str) -> UserEntity:
        try:
            updated_user = await self.repo.update_username(public_id, username)
        except UserNotFoundError:
            raise
        except Exception as exc:
            raise UsernameUpdateError() from exc

        return updated_user