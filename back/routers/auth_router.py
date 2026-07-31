from fastapi import APIRouter, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db import get_session

from schemas.auth.send_code_request import SendCodeRequest
from schemas.auth.verify_code_request import VerifyCodeRequest
from schemas.auth.refresh_request import RefreshRequest
from schemas.auth.logout_request import LogoutRequest
from schemas.auth.refresh_token_response import RefreshTokenResponse

from auth.core.errors.errors import InvalidVerificationCodeError

from di.auth_providers import (
    get_validate_email_uc,
    get_send_code_uc,
    get_verify_code_uc,
    get_generate_refresh_token_uc,
    get_generate_access_token_uc,
    get_rotate_refresh_token_uc,
    get_logout_refresh_token_uc,
)

ACCESS_TOKEN_MAX_AGE = 15 * 60

router = APIRouter()


def _set_access_cookie(response: Response, access_token: str) -> None:
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=ACCESS_TOKEN_MAX_AGE,
        httponly=True,
        secure=True,
        samesite="lax",
        path="/",
    )


@router.post("/send-code/")
async def send_code(
    payload: SendCodeRequest,
    session: AsyncSession = Depends(get_session),
):
    validate_email_uc = get_validate_email_uc(session)
    send_code_uc = get_send_code_uc()
    await validate_email_uc.execute(payload.email)
    return await send_code_uc.execute(payload.email)


@router.post("/verify-code/", response_model=RefreshTokenResponse)
async def verify_code(
    payload: VerifyCodeRequest,
    response: Response,
    session: AsyncSession = Depends(get_session),
):
    verify_code_uc = get_verify_code_uc(session)
    generate_refresh_uc = get_generate_refresh_token_uc()
    generate_access_uc = get_generate_access_token_uc()

    user_identity = await verify_code_uc.execute(
        email=payload.email,
        code=payload.code,
    )

    if user_identity is None:
        raise InvalidVerificationCodeError()

    refresh_token_entity = await generate_refresh_uc.execute(user_identity)
    access_token = await generate_access_uc.execute(refresh_token_entity)

    _set_access_cookie(response, access_token)

    return RefreshTokenResponse(refresh_token=refresh_token_entity.token)


@router.post("/refresh/", response_model=RefreshTokenResponse)
async def refresh_token(
    payload: RefreshRequest,
    response: Response,
):
    rotate_uc = get_rotate_refresh_token_uc()
    generate_access_uc = get_generate_access_token_uc()

    rotated = await rotate_uc.execute(payload.refresh_token)
    access_token = await generate_access_uc.execute(rotated)

    _set_access_cookie(response, access_token)

    return RefreshTokenResponse(refresh_token=rotated.token)


@router.post("/log-out/")
async def logout(
    payload: LogoutRequest,
    response: Response,
):
    logout_uc = get_logout_refresh_token_uc()
    await logout_uc.execute(payload.refresh_token)
    response.delete_cookie("access_token", path="/")
    return {"detail": "Logged out"}
