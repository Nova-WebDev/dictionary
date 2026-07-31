from pydantic import BaseModel

from dictionary.core.entities.word_order_field import WordOrderField


class GetWordsQuery(BaseModel):
    page: int = 1
    limit: int = 20
    search: str = ""
    order_by: WordOrderField = "created_at"
    descending: bool = True