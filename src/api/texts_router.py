from typing import Optional
from fastapi import APIRouter, HTTPException
import os

from src.core.parser.parser_factory import ParserFactory
from src.core.processor.natasha_processor import TextProcessor
from src.database.transactions import (
    insert_text,
    insert_sentences,
    create_tables,
    select_text_titles,
    select_text,
    select_all_text_info,
    update_text_content
)
from src.schemas.text_schemas import TextSchema
from src.schemas.sentence_schemas import SentenceSchema

router = APIRouter()
@router.get("/texts/text_titles", tags=['Texts'])
def get_texts_titles():
    '''Получение всех текстов'''
    text_titles = select_text_titles()
    if  text_titles == {}:
        raise HTTPException(status_code=404, detail=f'Do not find text titles')
    return {'data': text_titles}

@router.get('/texts/concrete_text', tags=['Texts'])
def get_text(text_id: int):
    '''Получение текста по id'''
    text = select_text(text_id)
    if not text:
        raise HTTPException(status_code=404, detail=f'Do not find text with such ID: {text_id}')
    return {'data': text}

@router.get('/texts/text_info', tags=['Texts'])
def get_text_info(text_id: int):
    text_info = select_all_text_info(text_id)
    if not text_info:
        raise HTTPException(status_code=404, detail=f'Do not find info of the text with such ID: {text_id}')
    return {'data': text_info}

@router.post("/texts/upload_file/{title}", tags=['Texts'])
def load_file(file_path: str, title: str):
    '''Загрузка файла с текстом, + название текста'''
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    parser = ParserFactory.get_parser(file_path)
    text = parser.parse(file_path)
    try:
        text_schema = TextSchema(content=text, title=title)
        text_id = insert_text(text=text_schema)
        processor = TextProcessor()
        sentences = processor.get_sentences(text)['sentences']
        sentence_schemas = [SentenceSchema(sentence=sentence['sentence']) for sentence in sentences]
        insert_sentences(text_id=text_id, sentences=sentence_schemas)
    except Exception:
        raise HTTPException(status_code=409, detail='A text with this title already exists')
    return {'message': 'File was loaded successfully'}







