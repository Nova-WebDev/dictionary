from pydantic import BaseModel


class CreateWordRequest(BaseModel):
    persian_word: str
    english_word: str