from fastapi import APIRouter
from api.words import router as words_router

main_router = APIRouter()
main_router.include_router(words_router)