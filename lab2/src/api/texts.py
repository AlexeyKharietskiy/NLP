from typing import Optional
from fastapi import APIRouter, HTTPException
import os

from core.text.concordances import get_concordances
from core.text.text_converter_factory import ParserFactory
from core.text.text_processor import processor
from core.transactions import (
    insert_text, 
    insert_words, 
    create_tables,
    select_texts,
    delete_text_by_id,
    update_text_content
)
from schemas.texts import TextSchema

router = APIRouter()

# d:\Project\sem6\ЕЯзИИС\lab1\data\test_data.docx
# d:\Project\sem6\ЕЯзИИС\lab1\data\test_data2.docx
@router.post("/upload_file/{title}", tags=['Insert'])
def load_file(file_path: str, title: str):
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    parser = ParserFactory.get_parser(file_path)
    text = parser.parse(file_path)
    try:
        text_schema = TextSchema(content=text, title=title)
        text_id = insert_text(text=text_schema)
        words = processor.get_tokens(text)
        insert_words(words=words, text_id=text_id)
    except Exception:
        raise HTTPException(status_code=409, detail='A text with this title already exists')
    return {'message': 'File was loaded successfully'}

@router.post("/upload_text", tags=['Insert'])
def load_text(text: str, title: str):
    text_schema = TextSchema(content=text, title=title)
    text_id = insert_text(text=text_schema)
    words = processor.get_tokens(text)
    insert_words(words=words, text_id=text_id)
    return {'message': 'Text was successfully loaded'}

@router.get("/get_texts", tags=['Select'])
def get_texts():
    texts = select_texts()
    return texts

@router.delete('/delete_text/{text_id}', tags=['Delete'])
def delete_text(text_id: int):
    delete_text_by_id(text_id)
    return {'message': f'Successfully delete text with text_id: {text_id}'}

@router.post('/change_text_content/{text_id}', tags=['Update'])
def change_text_content(text_id: int, new_content:Optional[str]=None, new_title:Optional[str]=None):
    update_text_content(text_id=text_id, new_content=new_content, new_title=new_title)
    if new_content:
        words = processor.get_tokens(new_content)
        insert_words(words=words, text_id=text_id)
    return {'message': f'Successfully update text with text_id: {text_id}'}