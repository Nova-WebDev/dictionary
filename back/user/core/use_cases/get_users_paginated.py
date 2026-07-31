from user.core.interfaces.user_repository import IUserRepository
from user.core.entities.user_order_field import UserOrderField


class GetUsersPaginatedUC:
    def __init__(self, repo: IUserRepository):
        self.repo = repo

    async def execute(
        self,
        page: int,
        limit: int,
        search: str,
        current_user_public_id: str,
        order_by: UserOrderField,
        descending: bool,
        include_self: bool,
    ) -> dict:
        if page < 1 or limit < 1:
            return {"users": [], "total_count": 0}

        offset = (page - 1) * limit
        exclude_id = None if include_self else current_user_public_id

        total_count = await self.repo.count_users(
            search=search, exclude_public_id=exclude_id
        )
        users = await self.repo.get_users_paginated(
            offset=offset,
            limit=limit,
            search=search,
            exclude_public_id=exclude_id,
            order_by=order_by,
            descending=descending,
        )

        return {"users": users, "total_count": total_count}