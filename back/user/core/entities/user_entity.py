from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserEntity:
    public_id: str
    email: str
    username: str | None
    role: int
    is_blocked: bool
    created_at: datetime