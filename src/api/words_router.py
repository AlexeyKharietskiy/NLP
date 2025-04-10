from fastapi import APIRouter

from schemas.sentence_schemas import SentenceSchema
from core.processor.natasha_processor import TextProcessor
from schemas.word_schemas import WordSchema
from database.transactions import (
    insert_words,
    select_words,
     select_words_by_rel,
     select_words_by_substr,
)
router = APIRouter()

@router.get('/words/{sentence_id}', tags=['Words'])
def get_words(sentence_id: int):
    words = select_words(sent_id=sentence_id)
    return {'data': words}

@router.get('/words/rel/{sentence_id}', tags=['Words'])
def get_words_by_rel(sentence_id: int, rel: str):
    words = select_words_by_rel(sentence_id=sentence_id, rel=rel)
    return {'data': words}

@router.get('/words/substr/{sentence_id}', tags=['Words'])
def get_words_by_substr(sentence_id: int, substr: str):
    words = select_words_by_substr(sentence_id=sentence_id, substr=substr)
    return {'data': words}