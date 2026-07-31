from pydantic import BaseModel


class BlockUserRequest(BaseModel):
    block: bool