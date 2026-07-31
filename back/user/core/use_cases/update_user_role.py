from user.core.entities.user_entity import UserEntity
from user.core.errors.errors import InvalidRoleError, PermissionDeniedError, UserNotFoundError
from user.core.interfaces.role_sync import IRoleSync
from user.core.interfaces.user_repository import IUserRepository



class UpdateUserRoleUC:
    def __init__(self, repo: IUserRepository, role_sync: IRoleSync):
        self.repo = repo
        self.role_sync = role_sync

    async def execute(
        self,
        requester_role: int,
        target_public_id: str,
        new_role: int,
    ) -> UserEntity:
        if requester_role != 20:
            raise PermissionDeniedError()

        if new_role < 1 or new_role >= 20:
            raise InvalidRoleError()

        target_user = await self.repo.get_by_public_id(target_public_id)
        if target_user is None:
            raise UserNotFoundError()

        if target_user.role >= requester_role:
            raise PermissionDeniedError()

        updated_user = await self.repo.update_role(
            public_id=target_public_id,
            new_role=new_role,
        )

        await self.role_sync.set_role(target_public_id, new_role)

        return updated_user