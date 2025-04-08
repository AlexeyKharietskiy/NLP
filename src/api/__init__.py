from fastapi import APIRouter
from src.api.texts_router import router as text_router
from src.api.words_router import router as word_router
from src.api.sentences_router import router as sentence_router


main_router = APIRouter()
main_router.include_router(text_router)
main_router.include_router(word_router)
main_router.include_router(sentence_router)