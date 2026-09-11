from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    email: str = Field(pattern=r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
    role: int
