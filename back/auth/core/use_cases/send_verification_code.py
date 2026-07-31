from auth.core.errors.errors import EmailTemporarilyBlockedError
from auth.core.interfaces.block_service import IBlockService
from auth.core.interfaces.code_generator import ICodeGenerator
from auth.core.interfaces.code_store import ICodeStore
from auth.core.interfaces.email_sender import IEmailSender


class SendVerificationCode:
    def __init__(
        self,
        block_service: IBlockService,
        code_generator: ICodeGenerator,
        code_store: ICodeStore,
        email_sender: IEmailSender
    ):
        self.block_service = block_service
        self.code_generator = code_generator
        self.code_store = code_store
        self.email_sender = email_sender

    async def execute(self, email: str):
        if await self.block_service.is_blocked(email):
            raise EmailTemporarilyBlockedError()
        await self.block_service.block(email, 60)
        code = await self.code_generator.generate()
        await self.code_store.save(email, code)
        await self.email_sender.send(email, code)

        return {"email": email, "sent": True}