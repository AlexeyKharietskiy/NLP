from fastapi import APIRouter, HTTPException
import os

from core.text.concordances import get_concordances
from core.text.text_converter_factory import ParserFactory
from core.text.text_processor import processor
from core.transactions import (
    insert_text, 
    insert_words, 
    create_tables,
    select_text,
    select_texts,
    select_words_from_text,
    select_word_by_pos,
    select_words_by_content,
)
from schemas.texts import TextSchema

router = APIRouter()

# d:\Project\sem6\ЕЯзИИС\lab1\data\test_data.docx
# d:\Project\sem6\ЕЯзИИС\lab1\data\test_data2.docx
@router.post("/upload_file", tags=['Insert'])
def load_file(file_path: str, title: str):
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    parser = ParserFactory.get_parser(file_path)
    text = parser.parse(file_path)
    text_schema = TextSchema(content=text, title=title)
    create_tables()
    text_id = insert_text(text=text_schema)
    words = processor.get_tokens(text)
    insert_words(words=words, text_id=text_id)
    return {'message': 'File was loaded successfully'}

@router.post("/upload_text", tags=['Insert'])
def load_text(text: str, title: str):
    text_schema = TextSchema(content=text, title=title)
    create_tables()
    text_id = insert_text(text=text_schema)
    words = processor.get_tokens(text)
    insert_words(words=words, text_id=text_id)
    return {'message': 'Text was successfully loaded'}

@router.get("/get_texts", tags=['Select'])
def get_texts():
    texts = select_texts()
    return texts

@router.get("/get_text_words/{text_id}", tags=['Select'])
def get_all_text_words(text_id: int):
    words = select_words_from_text(text_id=text_id)
    return words

@router.get("/get_text_words_with_pos/{text_id}/{pos}", tags=['Select'])
def get_text_words_with_pos(text_id: int, pos: str):
    words = select_word_by_pos(text_id=text_id, pos=pos.lower())
    return words

@router.get("/get_text_words_by_content/{text_id}", tags=['Select'])
def get_text_words_by_content(text_id: int, content: str):
    words = select_words_by_content(text_id=text_id, content=content.lower())
    return words

@router.get("/get_concordances/{word}", tags=['Concordance'])
def get_text_concordances(word: str):
    texts = select_texts()
    concordances = get_concordances(texts, word)
    return concordances