from typing import Optional
from fastapi import APIRouter, HTTPException
import os

from core.text.text_converter_factory import ParserFactory
from core.text.text_processor import processor
from core.transactions import (
    insert_text, 
    insert_words, 
    create_tables,
    select_texts,
    select_text_by_id,
    delete_text_by_id,
    update_text_values
)
from schemas.texts import TextSchema
router = APIRouter()
@router.post("/texts/upload_file/{title}", tags=['Texts'])
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

@router.get('/texts/concrete_text', tags=['Texts'])
def get_text(text_id: int):
    text = select_text_by_id(text_id)
    if not text:
        raise HTTPException(status_code=404, detail=f'Do not find text with such ID: {text_id}')
    return {'data': text}
    
@router.get("/texts", tags=['Texts'])
def get_texts():
    texts = select_texts()
    return {'data': texts}

@router.delete('/texts/delete_concrete_text', tags=['Texts'])
def delete_text(text_id: int):
    try:
        delete_text_by_id(text_id)
    except ValueError:
        HTTPException(status_code=404, detail=f'Do not find text with such ID: {text_id}') 
    return {'message': f'Successfully delete text with text_id: {text_id}'}

@router.post('/texts/update_concrete_text', tags=['Update'])
def update_text(text_id: int, new_content:Optional[str]=None, new_title:Optional[str]=None):
    try:
        update_text_values(text_id=text_id, new_content=new_content, new_title=new_title)
        if new_content:
            words = processor.get_tokens(new_content)
            insert_words(words=words, text_id=text_id)
    except ValueError:
        HTTPException(status_code=404, detail=f'Do not find text with such ID: {text_id}')
    return {'message': f'Successfully update text with id: {text_id}'}