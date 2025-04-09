from fastapi import APIRouter

from database.transactions import select_sentences

router = APIRouter()

@router.get('/sentences/{text_id}', tags=['Sentences'])
def get_sentences(text_id: int):
    sents = select_sentences(text_id)
    return {"data": sents}