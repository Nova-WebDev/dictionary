from auth.core.interfaces.refresh_token_store import IRefreshTokenStore


class LogoutRefreshToken:
    def __init__(self, store: IRefreshTokenStore):
        self.store = store

    async def execute(self, refresh_token_str: str) -> None:
        await self.store.delete(refresh_token_str)