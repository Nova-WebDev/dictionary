from typing import Protocol


class IRoleSync(Protocol):
    async def set_role(self, public_id: str, role: int) -> None: ...