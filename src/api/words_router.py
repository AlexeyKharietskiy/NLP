from fastapi import APIRouter, HTTPException

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
    """Get all sentence words

    Args:
        sentence_id (int): selected sentence id from database

    Raises:
        HTTPException: do not find any words with given params

    Returns:
        data: [
            {
                "id": int,
                "sentence_id": int,
                "head": str,
                "word": str,
                "relation": str
            }     
        ]
    """
    words = select_words(sent_id=sentence_id)
    if not words:
        raise HTTPException(status_code=404, detail=f"Do not have any words in sentence {sentence_id}")
    return {'data': words}

@router.get('/words/rel/{sentence_id}', tags=['Words'])
def get_words_by_rel(sentence_id: int, rel: str):
    """Get sentence words with given relation

    Args:
        sentence_id (int): selected sentence id from database
        rel (str): selected relation

    Raises:
        HTTPException: do not find any words with given params

    Returns:
        data: [
            {
                "id": int,
                "sentence_id": int,
                "head": str,
                "word": str,
                "relation": str
            }     
        ]
    """
    words = select_words_by_rel(sentence_id=sentence_id, rel=rel)
    if not words:
        raise HTTPException(
            status_code=404, 
            detail=f"Do not have any words in sentence {sentence_id} by relation: {rel}"
        )
    return {'data': words}

@router.get('/words/substr/{sentence_id}', tags=['Words'])
def get_words_by_substr(sentence_id: int, substr: str):
    """Get sentence words with given substr

    Args:
        sentence_id (int): selected sentence id from database
        substr (str): searched substr

    Raises:
        HTTPException: do not find any words with given params

    Returns:
        data: [
            {
                "id": int,
                "sentence_id": int,
                "head": str,
                "word": str,
                "relation": str
            }     
        ]
    """
    words = select_words_by_substr(sentence_id=sentence_id, substr=substr)
    if not words:
        raise HTTPException(
            status_code=404, 
            detail=f"Do not have any words in sentence {sentence_id} by substr: {substr}"
        )
    return {'data': words}