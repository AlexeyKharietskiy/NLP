from fastapi import APIRouter, HTTPException


from core.text.concordances import get_concordances
from core.transactions import (

    select_texts,
)
from schemas.texts import TextSchema

router = APIRouter()

@router.get("/concordances/{word}", tags=['Concordances'])
def get_text_concordances(word: str):
    texts = select_texts()
    concordances = get_concordances(texts, word)
    if not concordances:
        raise HTTPException(status_code=404, detail=f'Did not find word: {word}')
    return {'data': concordances}