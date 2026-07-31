from auth.core.errors.errors import (
    EmailBlockedError,
    EmailDomainNotAllowedError,
    InvalidEmailFormatError,
)
from auth.core.interfaces.email_block_checker import IEmailBlockChecker


class ValidateEmail:
    def __init__(self, allowed_domains: list[str], blocklist_checker: IEmailBlockChecker):
        self.allowed_domains = allowed_domains
        self.blocklist_checker = blocklist_checker

    async def execute(self, email: str) -> None:
        try:
            local, domain = email.split("@")
        except ValueError:
            raise InvalidEmailFormatError()

        if domain not in self.allowed_domains:
            raise EmailDomainNotAllowedError()

        if await self.blocklist_checker.is_blocked(email):
            raise EmailBlockedError()