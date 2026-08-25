from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.data.db import get_session
from app.security.dependencies import get_current_user

from schemas.dictionary.create_word_request import CreateWordRequest
from schemas.dictionary.edit_word_request import EditWordRequest
from schemas.dictionary.get_words_query import GetWordsQuery
from schemas.dictionary.search_word_query import SearchWordQuery

from di.dictionary_providers import (
    get_create_word_entry_uc,
    get_search_english_to_persian_uc,
    get_search_persian_to_english_uc,
    get_words_paginated_uc,
)
from di.cross_domain_providers import (
    get_delete_word_entry_uc,
    get_edit_word_entry_uc,
)

router = APIRouter()


@router.get("/search/persian-to-english")
async def search_persian_to_english(
    query: SearchWordQuery = Depends(),
    session: AsyncSession = Depends(get_session),
    _user: dict = Depends(get_current_user),
):
    uc = get_search_persian_to_english_uc(session)
    return await uc.execute(query.q)


@router.get("/search/english-to-persian")
async def search_english_to_persian(
    query: SearchWordQuery = Depends(),
    session: AsyncSession = Depends(get_session),
    _user: dict = Depends(get_current_user),
):
    uc = get_search_english_to_persian_uc(session)
    return await uc.execute(query.q)


@router.get("/")
async def get_words(
    query: GetWordsQuery = Depends(),
    session: AsyncSession = Depends(get_session),
    _user: dict = Depends(get_current_user),
):
    uc = get_words_paginated_uc(session)
    return await uc.execute(
        page=query.page,
        limit=query.limit,
        search=query.search,
        order_by=query.order_by,
        descending=query.descending,
    )


@router.post("/")
async def create_word(
    payload: CreateWordRequest,
    session: AsyncSession = Depends(get_session),
    _user: dict = Depends(get_current_user),
):
    uc = get_create_word_entry_uc(session)
    return await uc.execute(
        requester_role=_user["role"],
        author_id=_user["public_id"],
        persian_word=payload.persian_word,
        english_word=payload.english_word,
    )


@router.patch("/{public_id}")
async def edit_word(
    public_id: str,
    payload: EditWordRequest,
    session: AsyncSession = Depends(get_session),
    _user: dict = Depends(get_current_user),
):
    uc = get_edit_word_entry_uc(session)
    return await uc.execute(
        requester_role=_user["role"],
        public_id=public_id,
        persian_word=payload.persian_word,
        english_word=payload.english_word,
    )


@router.delete("/{public_id}")
async def delete_word(
    public_id: str,
    session: AsyncSession = Depends(get_session),
    _user: dict = Depends(get_current_user),
):
    uc = get_delete_word_entry_uc(session)
    await uc.execute(
        requester_role=_user["role"],
        public_id=public_id,
    )
    return {"detail": "Word deleted"}