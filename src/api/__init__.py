from fastapi import APIRouter
from api.words import router as words_router
from api.concordances import router as concord_router
from api.texts import router as texts_router

main_router = APIRouter()
main_router.include_router(words_router)
main_router.include_router(texts_router)
main_router.include_router(concord_router)