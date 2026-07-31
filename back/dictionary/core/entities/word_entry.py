from dataclasses import dataclass
from datetime import datetime


@dataclass
class WordEntryEntity:
    public_id: str
    persian_word: str
    english_word: str
    author_id: str | None
    created_at: datetime