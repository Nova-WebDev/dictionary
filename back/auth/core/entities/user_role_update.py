from dataclasses import dataclass

@dataclass
class UserRoleUpdate:
    public_id: str
    role: int
