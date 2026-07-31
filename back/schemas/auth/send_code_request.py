from pydantic import BaseModel


class SendCodeRequest(BaseModel):
    email: str