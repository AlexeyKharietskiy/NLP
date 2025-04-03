from fastapi import APIRouter, HTTPException


from core.text.concordances import get_concordances
from core.transactions import (

    select_texts,
)
from schemas.texts import TextSchema

router = APIRouter()

@router.get("/get_concordances/{word}", tags=['Concordance'])
def get_text_concordances(word: str):
    texts = select_texts()
    concordances = get_concordances(texts, word)
    return concordances