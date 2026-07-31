from pydantic import BaseModel


class UpdateUsernameRequest(BaseModel):
    username: str