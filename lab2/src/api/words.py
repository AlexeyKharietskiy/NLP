from fastapi import APIRouter, HTTPException
from core.transactions import (
    select_words_from_text,
    select_word_by_pos,
    select_words_by_content,
)

router = APIRouter()


@router.get("/get_text_words/{text_id}", tags=['Select'])
def get_all_text_words(text_id: int):
    words = select_words_from_text(text_id=text_id)
    return words

@router.get("/get_text_words_with_pos/{text_id}/{pos}", tags=['Select'])
def get_text_words_with_pos(text_id: int, pos: str):
    words = select_word_by_pos(text_id=text_id, pos=pos.lower())
    return words

@router.get("/get_text_words_by_content/{text_id}", tags=['Select'])
def get_text_words_by_content(text_id: int, content: str):
    words = select_words_by_content(text_id=text_id, content=content.lower())
    return words