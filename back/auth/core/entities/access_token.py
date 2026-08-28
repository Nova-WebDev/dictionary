from dataclasses import dataclass


@dataclass
class AccessToken:
    token: str
    expires_at: int