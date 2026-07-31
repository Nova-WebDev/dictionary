from pydantic import BaseModel


class RefreshTokenResponse(BaseModel):
    refresh_token: str