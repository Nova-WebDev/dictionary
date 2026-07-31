from dataclasses import dataclass

@dataclass
class UserBlockStatus:
    public_id: str
    is_blocked: bool
