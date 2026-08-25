from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db import get_session
from app.security.dependencies import get_current_user

from schemas.user.block_user_request import BlockUserRequest
from schemas.user.get_users_query import GetUsersQuery
from schemas.user.update_role_request import UpdateRoleRequest
from schemas.user.update_username_request import UpdateUsernameRequest

from di.user_providers import (
    get_user_profile_uc,
    get_users_paginated_uc,
    get_update_username_uc,
)
from di.cross_domain_providers import (
    get_block_or_unblock_user_uc,
    get_update_user_role_uc,
)

router = APIRouter()


@router.get("/me")
async def get_my_profile(
    session: AsyncSession = Depends(get_session),
    _user: dict = Depends(get_current_user),
):
    uc = get_user_profile_uc(session)
    return await uc.execute(_user["public_id"])


@router.get("/{public_id}")
async def get_user_profile(
    public_id: str,
    session: AsyncSession = Depends(get_session),
    _user: dict = Depends(get_current_user),
):
    uc = get_user_profile_uc(session)
    return await uc.execute(public_id)


@router.get("/")
async def get_users(
    query: GetUsersQuery = Depends(),
    session: AsyncSession = Depends(get_session),
    _user: dict = Depends(get_current_user),
):
    uc = get_users_paginated_uc(session)
    return await uc.execute(
        page=query.page,
        limit=query.limit,
        search=query.search,
        current_user_public_id=_user["public_id"],
        order_by=query.order_by,
        descending=query.descending,
        include_self=query.include_self,
    )


@router.patch("/me/username")
async def update_my_username(
    payload: UpdateUsernameRequest,
    session: AsyncSession = Depends(get_session),
    _user: dict = Depends(get_current_user),
):
    uc = get_update_username_uc(session)
    return await uc.execute(_user["public_id"], payload.username)


@router.patch("/{public_id}/block")
async def block_or_unblock_user(
    public_id: str,
    payload: BlockUserRequest,
    session: AsyncSession = Depends(get_session),
    _user: dict = Depends(get_current_user),
):
    uc = get_block_or_unblock_user_uc(session)
    return await uc.execute(
        requester_role=_user["role"],
        target_public_id=public_id,
        block=payload.block,
    )


@router.patch("/{public_id}/role")
async def update_user_role(
    public_id: str,
    payload: UpdateRoleRequest,
    session: AsyncSession = Depends(get_session),
    _user: dict = Depends(get_current_user),
):
    uc = get_update_user_role_uc(session)
    return await uc.execute(
        requester_role=_user["role"],
        target_public_id=public_id,
        new_role=payload.new_role,
    )