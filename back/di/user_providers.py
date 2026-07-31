from sqlalchemy.ext.asyncio import AsyncSession

from user.infrastructure.data.user_repository import UserRepository

from user.core.use_cases.get_user_profile import GetUserProfileByPublicIdUC
from user.core.use_cases.get_users_paginated import GetUsersPaginatedUC
from user.core.use_cases.update_username import UpdateUsernameUC


def get_user_profile_uc(session: AsyncSession) -> GetUserProfileByPublicIdUC:
    return GetUserProfileByPublicIdUC(repo=UserRepository(session))


def get_users_paginated_uc(session: AsyncSession) -> GetUsersPaginatedUC:
    return GetUsersPaginatedUC(repo=UserRepository(session))


def get_update_username_uc(session: AsyncSession) -> UpdateUsernameUC:
    return UpdateUsernameUC(repo=UserRepository(session))