from user.core.entities.user_entity import UserEntity
from user.core.errors.errors import PermissionDeniedError, UserNotFoundError
from user.core.interfaces.block_status_sync import IBlockStatusSync
from user.core.interfaces.user_repository import IUserRepository


class BlockOrUnblockUserUC:
    def __init__(self, repo: IUserRepository, block_status_sync: IBlockStatusSync):
        self.repo = repo
        self.block_status_sync = block_status_sync

    async def execute(
        self,
        requester_role: int,
        target_public_id: str,
        block: bool,
    ) -> UserEntity:
        target_user = await self.repo.get_by_public_id(target_public_id)
        if target_user is None:
            raise UserNotFoundError()

        if requester_role <= target_user.role:
            raise PermissionDeniedError()

        updated_user = await self.repo.update_block_status(
            public_id=target_public_id,
            is_blocked=block,
        )

        if block:
            await self.block_status_sync.block(target_public_id)
        else:
            await self.block_status_sync.unblock(target_public_id)

        return updated_user