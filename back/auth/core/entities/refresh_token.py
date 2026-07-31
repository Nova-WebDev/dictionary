from dataclasses import dataclass

@dataclass
class RefreshToken:
    token: str
    public_id: str
    role: int
    email:str
