from pydantic import BaseModel


class RefreshTokenResponse(BaseModel):
    refresh_token: str
    access_token_expires_at: int