from pydantic import BaseModel

from user.core.entities.user_order_field import UserOrderField


class GetUsersQuery(BaseModel):
    page: int = 1
    limit: int = 20
    search: str = ""
    order_by: UserOrderField = "created_at"
    descending: bool = True
    include_self: bool = False