from sqlalchemy.ext.asyncio import AsyncSession

from app.redis.redis_client import redis_client

from auth.infrastructure.store.user_remove_store import UserRemoveStore
from auth.infrastructure.store.user_role_store import UserRoleStore

from user.infrastructure.data.user_repository import UserRepository

from dictionary.infrastructure.data.word_repository import WordRepository

from user.core.use_cases.block_or_unblock_user import BlockOrUnblockUserUC
from user.core.use_cases.update_user_role import UpdateUserRoleUC

from dictionary.core.use_cases.delete_word_entry import DeleteWordEntryUC
from dictionary.core.use_cases.edit_word_entry import EditWordEntryUC


def get_block_or_unblock_user_uc(session: AsyncSession) -> BlockOrUnblockUserUC:
    return BlockOrUnblockUserUC(
        repo=UserRepository(session),
        block_status_sync=UserRemoveStore(redis_client),
    )


def get_update_user_role_uc(session: AsyncSession) -> UpdateUserRoleUC:
    return UpdateUserRoleUC(
        repo=UserRepository(session),
        role_sync=UserRoleStore(redis_client),
    )



def get_edit_word_entry_uc(session: AsyncSession) -> EditWordEntryUC:
    return EditWordEntryUC(
        repo=WordRepository(session),
        user_lookup=UserRepository(session),
        min_role_when_author_unknown=10,
    )


def get_delete_word_entry_uc(session: AsyncSession) -> DeleteWordEntryUC:
    return DeleteWordEntryUC(
        repo=WordRepository(session),
        user_lookup=UserRepository(session),
        min_role_when_author_unknown=10,
    )