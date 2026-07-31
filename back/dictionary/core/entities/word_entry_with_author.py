from dataclasses import dataclass
from datetime import datetime


@dataclass
class WordEntryWithAuthorEntity:
    public_id: str
    persian_word: str
    english_word: str
    author_name: str | None
    created_at: datetime