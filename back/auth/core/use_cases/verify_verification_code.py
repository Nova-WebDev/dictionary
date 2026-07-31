from auth.core.entities.user_identity import UserIdentity
from auth.core.interfaces.attempt_counter import IAttemptCounter
from auth.core.interfaces.block_service import IBlockService
from auth.core.interfaces.code_store import ICodeStore
from auth.core.interfaces.user_service import IUserService


class VerifyVerificationCode:
    def __init__(
        self,
        code_store: ICodeStore,
        block_service: IBlockService,
        attempt_counter: IAttemptCounter,
        user_service: IUserService,
        max_attempts: int = 5,
    ):
        self.code_store = code_store
        self.block_service = block_service
        self.attempt_counter = attempt_counter
        self.user_service = user_service
        self.max_attempts = max_attempts

    async def execute(self, email: str, code: str) -> UserIdentity | None:
        stored_code = await self.code_store.get(email)

        if stored_code is None:
            attempts = await self.attempt_counter.increment(email)

            if attempts >= self.max_attempts:
                await self.block_service.block(email, 300)
                await self.code_store.delete(email)

            return None

        if code == stored_code:
            await self.code_store.delete(email)
            user_identity = await self.user_service.create_user(email)
            return user_identity

        attempts = await self.attempt_counter.increment(email)

        if attempts >= self.max_attempts:
            await self.block_service.block(email, 300)
            await self.code_store.delete(email)

        return None