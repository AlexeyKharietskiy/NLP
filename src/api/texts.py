import json
from typing import Optional
from fastapi import APIRouter, Body, HTTPException
import os

from core.text.text_converter_factory import ParserFactory
from core.text.text_processor import processor
from core.transactions import (
    insert_text, 
    insert_words, 
    create_tables,
    select_all_data,
    select_texts,
    select_text_by_id,
    delete_text_by_id,
    update_text_values
)
from schemas.texts import FilePathSchema, TextSchema
router = APIRouter()
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
        words = processor.get_tokens(text)
        insert_words(words=words, text_id=text_id)
    except Exception:
        raise HTTPException(status_code=409, detail='A text with this title already exists')
    return {'message': 'File was loaded successfully'}

@router.get('/texts/concrete_text', tags=['Texts'])
def get_text(text_id: int):
    '''Получение текста по id'''
    text = select_text_by_id(text_id)
    if not text:
        raise HTTPException(status_code=404, detail=f'Do not find text with such ID: {text_id}')
    return {'data': text}
    
@router.get("/texts", tags=['Texts'])
def get_texts():
    '''Получение всех текстов'''
    texts = select_texts()
    return {'data': texts}

@router.delete('/texts/delete_concrete_text', tags=['Texts'])
def delete_text(text_id: int):
    '''Удаление текста по id'''
    try:
        delete_text_by_id(text_id)
    except ValueError:
        HTTPException(status_code=404, detail=f'Do not find text with such ID: {text_id}') 
    return {'message': f'Successfully delete text with text_id: {text_id}'}

@router.post('/texts/update_concrete_text', tags=['Update'])
def update_text(req: TextSchema):
    '''Обновление текста, можно обновить как содержимое так и название, если изменили содержимое, то и словоформы меняются'''
    try:
        update_text_values(text_id=req.id, new_content=req.content, new_title=req.title)
        if req.content:
            words = processor.get_tokens(req.content)
            insert_words(words=words, text_id=req.id)
    except ValueError:
        HTTPException(status_code=404, detail=f'Do not find text with such ID: {req.id}')
    return {'message': f'Successfully update text with id: {req.id}'}

@router.post('/save_corpus', tags=['Corpus'])
def save_corpus(path: FilePathSchema):
    if not path.file_path:
        return {"message": "No file path provided"}
    corpus_texts = select_all_data()
    res = {
        'corpus': []
    }
    for text in corpus_texts:
        res['corpus'].append(
            {
                'title': text.title,
                'content': text.content,
                'created_at': text.create_at.isoformat(),
                'updated_at': text.updated_at.isoformat(),
                'words': [
                    {
                        'word': word.word,
                        'frequency': word.frequency,
                        'lemma': word.lemma,
                        'part_of_speech': word.part_of_speech,
                        'feats': word.feats,
                    }
                    for word in text.words
                ]
            }
        )
    try:
        with open(path.file_path, 'w', encoding='utf-8') as file:
            json.dump(res, file, ensure_ascii=False, indent=4)
        return {'message': f'File was saved to {path.file_path}!'}
    except Exception as e:
        return {'error': str(e)}