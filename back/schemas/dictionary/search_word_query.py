from pydantic import BaseModel


class SearchWordQuery(BaseModel):
    q: str