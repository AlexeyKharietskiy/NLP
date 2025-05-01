from fastapi import APIRouter, HTTPException

from database.transactions import select_sentences

router = APIRouter()

@router.get('/sentences/{text_id}', tags=['Sentences'])
def get_sentences(text_id: int):
    """Get all text sentences

    Args:
        text_id (int): selected text id from database

    Raises:
        HTTPException: text do not have any sentences

    Returns:
        data: [
            id: int,
            sentence: str,
            text_id: sentence
        ]
    """
    sents = select_sentences(text_id)
    if not sents:
        raise HTTPException(status_code=404, detail=f'Do not find any sentence by text id {text_id}')
    return {"data": sents}