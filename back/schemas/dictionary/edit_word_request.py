from pydantic import BaseModel


class EditWordRequest(BaseModel):
    persian_word: str
    english_word: str