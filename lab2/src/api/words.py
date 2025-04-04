from fastapi import APIRouter, HTTPException
from core.transactions import (
    select_words_from_text,
    select_word_by_pos,
    select_words_by_content,
)

router = APIRouter()


@router.get("/words/{text_id}", tags=['Words'])
def get_all_text_words(text_id: int):
    '''Получение всех слов из текста с заданным id'''
    words = select_words_from_text(text_id=text_id)
    return {'data': words}

@router.get("/words/pos/{text_id}", tags=['Words'])
def get_text_words_with_pos(text_id: int, pos: str):
    '''Получение всех слов с заданной частью речи из текста с заданным id'''
    words = select_word_by_pos(text_id=text_id, pos=pos.lower())
    return {'data': words}

@router.get("/words/wordform/{text_id}", tags=['Words'])
def get_text_words_by_content(text_id: int, content: str):
    '''Получение всех слов, содержащих заданную подстроку, из текста с заданным id'''
    try:
        words = select_words_by_content(text_id=text_id, content=content.lower())
    except ValueError:
        raise HTTPException(status_code=404, detail=f"No words found containing '{content}' in text with id: {text_id}")
    return {'data': words}