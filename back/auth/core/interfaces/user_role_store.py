from abc import ABC, abstractmethod


class IUserRoleStore(ABC):
    @abstractmethod
    async def set_role(self, public_id: str, role: int) -> None: ...

    @abstractmethod
    async def get_role(self, public_id: str) -> int | None: ...