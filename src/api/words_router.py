from fastapi import APIRouter, HTTPException

from database.transactions import (
    select_morphological_words,
    select_ners,
    select_syntax_words,
    select_words,
    select_words_by_pos,
    select_words_by_substr,
)
router = APIRouter()

@router.get('/syntax_words/{sentence_id}', tags=['Words'])
def get_syntax_words(sentence_id: int):
    words = select_syntax_words(sent_id=sentence_id)
    if not words:
        raise HTTPException(status_code=404, detail=f"Do not have any words in sentence {sentence_id}")
    return {'data': words}

@router.get('/morphological_words/{sentence_id}', tags=['Words'])
def get_morphological_words(sentence_id: int):
    words = select_morphological_words(sent_id=sentence_id)
    if not words:
        raise HTTPException(status_code=404, detail=f"Do not have any words in sentence {sentence_id}")
    return {'data': words}

@router.get('/ners/{sentence_id}', tags=['Words'])
def get_ners(sentence_id: int):
    words = select_ners(sent_id=sentence_id)
    if not words:
        raise HTTPException(status_code=404, detail=f"Do not have any ners in sentence {sentence_id}")
    return {'data': words}


@router.get('/words/pos/{sentence_id}', tags=['Words'])
def get_words_by_pos(sentence_id: int, pos: str):
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
    words = select_words_by_pos(sentence_id=sentence_id, pos=pos)
    if not words:
        raise HTTPException(
            status_code=404, 
            detail=f"Do not have any words in sentence {sentence_id} by pos: {pos}"
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