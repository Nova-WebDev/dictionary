from dataclasses import dataclass

@dataclass
class TokenPayload:
    email: str
    public_id: str
    role: int
    iat: int
    exp: int

