from sqlalchemy.ext.asyncio import AsyncSession

from app.redis.redis_client import redis_client
from app.settings import settings

from auth.infrastructure.signing.token_header_generator import TokenHeaderGenerator
from auth.infrastructure.signing.token_payload_generator import TokenPayloadGenerator
from auth.infrastructure.signing.token_signer import TokenSigner
from auth.infrastructure.store.refresh_token_store import RefreshTokenStore
from auth.infrastructure.store.user_remove_store import UserRemoveStore
from auth.infrastructure.store.user_role_store import UserRoleStore
from auth.infrastructure.data.email_block_repository import EmailBlockRepository
from auth.infrastructure.data.user_repository import UserRepository
from auth.infrastructure.email.email_sender import EmailSender
from auth.infrastructure.store.attempt_counter import AttemptCounter
from auth.infrastructure.store.block_service import BlockService
from auth.infrastructure.store.code_store import CodeStore

from auth.utility.secure_token_generator import SecureTokenGenerator
from auth.utility.code_generator import CodeGenerator

from auth.core.use_cases.generate_access_token import GenerateAccessToken
from auth.core.use_cases.generate_refresh_token import GenerateRefreshToken
from auth.core.use_cases.logout_refresh_token import LogoutRefreshToken
from auth.core.use_cases.rotate_refresh_token import RotateRefreshToken
from auth.core.use_cases.validate_email import ValidateEmail
from auth.core.use_cases.send_verification_code import SendVerificationCode
from auth.core.use_cases.verify_verification_code import VerifyVerificationCode


def get_generate_access_token_uc() -> GenerateAccessToken:
    return GenerateAccessToken(
        header_generator=TokenHeaderGenerator(),
        payload_generator=TokenPayloadGenerator(),
        signer=TokenSigner(),
    )


def get_generate_refresh_token_uc() -> GenerateRefreshToken:
    return GenerateRefreshToken(
        generator=SecureTokenGenerator(32),
        store=RefreshTokenStore(redis_client),
    )


def get_logout_refresh_token_uc() -> LogoutRefreshToken:
    return LogoutRefreshToken(
        store=RefreshTokenStore(redis_client),
    )


def get_rotate_refresh_token_uc() -> RotateRefreshToken:
    return RotateRefreshToken(
        store=RefreshTokenStore(redis_client),
        generator=SecureTokenGenerator(32),
        remove_store=UserRemoveStore(redis_client),
        role_store=UserRoleStore(redis_client),
    )


def get_validate_email_uc(session: AsyncSession) -> ValidateEmail:
    return ValidateEmail(
        allowed_domains=settings.allowed_domains,
        blocklist_checker=EmailBlockRepository(session),
    )


def get_send_code_uc() -> SendVerificationCode:
    return SendVerificationCode(
        block_service=BlockService(redis_client),
        code_generator=CodeGenerator(5),
        code_store=CodeStore(redis_client),
        email_sender=EmailSender(),
    )


def get_verify_code_uc(session: AsyncSession) -> VerifyVerificationCode:
    return VerifyVerificationCode(
        code_store=CodeStore(redis_client),
        block_service=BlockService(redis_client),
        attempt_counter=AttemptCounter(redis_client),
        user_service=UserRepository(session),
        max_attempts=5,
    )