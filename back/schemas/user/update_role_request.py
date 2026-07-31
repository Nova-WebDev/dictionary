from pydantic import BaseModel


class UpdateRoleRequest(BaseModel):
    new_role: int