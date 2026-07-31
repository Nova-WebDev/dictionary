from sqlalchemy.ext.asyncio import AsyncSession

from dictionary.infrastructure.data.word_repository import WordRepository

from dictionary.core.use_cases.create_word_entry import CreateWordEntryUC
from dictionary.core.use_cases.get_words_paginated import GetWordsPaginatedUC
from dictionary.core.use_cases.search_english_to_persian import SearchEnglishToPersianUC
from dictionary.core.use_cases.search_persian_to_english import SearchPersianToEnglishUC


def get_search_persian_to_english_uc(session: AsyncSession) -> SearchPersianToEnglishUC:
    return SearchPersianToEnglishUC(repo=WordRepository(session))


def get_search_english_to_persian_uc(session: AsyncSession) -> SearchEnglishToPersianUC:
    return SearchEnglishToPersianUC(repo=WordRepository(session))


def get_create_word_entry_uc(session: AsyncSession) -> CreateWordEntryUC:
    return CreateWordEntryUC(repo=WordRepository(session), min_create_role=10)


def get_words_paginated_uc(session: AsyncSession) -> GetWordsPaginatedUC:
    return GetWordsPaginatedUC(repo=WordRepository(session))