from dataclasses import dataclass

@dataclass
class UserIdentity:
    email: str
    role: int
    public_id: str
