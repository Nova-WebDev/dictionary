from fastapi import HTTPException, status

from app.utils.logger import logger
from auth.core.errors.errors import (
    EmailBlockCheckError,
    EmailBlockedError,
    EmailDomainNotAllowedError,
    EmailTemporarilyBlockedError,
    InvalidEmailFormatError,
    InvalidRefreshTokenError,
    RefreshTokenPersistenceError,
    TokenGenerationError,
    UserBlockedError,
    UserCreationError,
    UserStatePersistenceError,
    InvalidVerificationCodeError,
)


def map_error(exc: Exception) -> HTTPException:
    if isinstance(exc, TokenGenerationError):
        logger.error("Token generation failed", exc_info=True)
        return HTTPException(status_code=500, detail=str(exc))

    if isinstance(exc, RefreshTokenPersistenceError):
        logger.error("Refresh token store failure", exc_info=True)
        return HTTPException(status_code=500, detail=str(exc))

    if isinstance(exc, InvalidRefreshTokenError):
        return HTTPException(status_code=401, detail=str(exc))

    if isinstance(exc, UserBlockedError):
        return HTTPException(status_code=403, detail=str(exc))

    if isinstance(exc, UserStatePersistenceError):
        logger.error("User state store failure", exc_info=True)
        return HTTPException(status_code=500, detail=str(exc))

    if isinstance(exc, InvalidEmailFormatError):
        return HTTPException(status_code=400, detail=str(exc))

    if isinstance(exc, EmailDomainNotAllowedError):
        return HTTPException(status_code=403, detail=str(exc))

    if isinstance(exc, EmailBlockedError):
        return HTTPException(status_code=403, detail=str(exc))

    if isinstance(exc, EmailBlockCheckError):
        logger.error("Email block check failed", exc_info=True)
        return HTTPException(status_code=500, detail=str(exc))

    if isinstance(exc, EmailTemporarilyBlockedError):
        return HTTPException(status_code=429, detail=str(exc))

    if isinstance(exc, UserCreationError):
        logger.error("User creation failed", exc_info=True)
        return HTTPException(status_code=500, detail=str(exc))

    if isinstance(exc, InvalidVerificationCodeError):
        return HTTPException(status_code=401, detail=str(exc))

    logger.error("Unhandled auth error", exc_info=True)
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Internal server error",
    )