from auth.core.entities.refresh_token import RefreshToken
from auth.core.errors.errors import (
    InvalidRefreshTokenError,
    RefreshTokenPersistenceError,
    UserBlockedError,
)
from auth.core.interfaces.refresh_token_store import IRefreshTokenStore
from auth.core.interfaces.token_generator import ITokenGenerator
from auth.core.interfaces.user_remove_store import IUserRemoveStore
from auth.core.interfaces.user_role_store import IUserRoleStore


class RotateRefreshToken:
    def __init__(
        self,
        store: IRefreshTokenStore,
        generator: ITokenGenerator,
        remove_store: IUserRemoveStore,
        role_store: IUserRoleStore,
    ):
        self.store = store
        self.generator = generator
        self.remove_store = remove_store
        self.role_store = role_store

    async def execute(self, refresh_token_str: str) -> RefreshToken:
        try:
            user_data = await self.store.get(refresh_token_str)
        except Exception as exc:
            raise RefreshTokenPersistenceError() from exc

        if user_data is None:
            raise InvalidRefreshTokenError()

        public_id = user_data["public_id"]

        try:
            is_blocked = await self.remove_store.is_blocked(public_id)
            new_role = await self.role_store.get_role(public_id)
        except Exception as exc:
            raise RefreshTokenPersistenceError() from exc

        if is_blocked:
            raise UserBlockedError()

        final_role = new_role if new_role is not None else user_data["role"]

        updated_user_data = {
            "public_id": public_id,
            "email": user_data["email"],
            "role": final_role,
        }

        new_token = await self.generator.generate()

        try:
            await self.store.delete(refresh_token_str)
            await self.store.save(new_token, updated_user_data)
        except Exception as exc:
            raise RefreshTokenPersistenceError() from exc

        return RefreshToken(
            token=new_token,
            public_id=public_id,
            role=final_role,
            email=user_data["email"],
        )