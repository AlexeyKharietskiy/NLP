import json
from typing import Optional
from fastapi import APIRouter, HTTPException
import os

from core.parser.parser_factory import ParserFactory
from core.processor.natasha_processor import TextProcessor
from database.transactions import (
    delete_sentences,
    insert_all_data,
    insert_sentences,
    create_tables,
    select_text_titles,
    select_text,
    select_all_text_info,
    update_text_content
)
from schemas.text_schemas import FilePathSchema, TextContentUpdateSchema, TextSchema
from schemas.sentence_schemas import SentenceSchema

router = APIRouter()
@router.get("/texts/text_titles", tags=['Texts'])
def get_texts_titles():
    '''Получение всех текстов'''
    text_titles = select_text_titles()
    if not text_titles:
        raise HTTPException(status_code=404, detail=f'Do not find text titles')
    return {'data': text_titles}

@router.get('/texts/concrete_text/{text_id}', tags=['Texts'])
def get_text(text_id: int):
    '''Получение текста по id'''
    text = select_text(text_id)
    if not text:
        raise HTTPException(status_code=404, detail=f'Do not find text with such ID: {text_id}')
    return {'data': text}

@router.post('/texts/save/{text_id}', tags=['Texts'])
def save_text_info(text_id: int, path: FilePathSchema):
    if not path.file_path:
        return {"message": "No file path provided"}
    text = select_all_text_info(text_id)
    
    if not text:
        raise HTTPException(status_code=404, detail=f'Do not find info of the text with such ID: {text_id}')
    res = {
        'text': []
    }
    res['text'].append(
        {
            'title': text.title,
            'content': text.content,
            'created_at': text.create_at.isoformat(),
            'updated_at': text.updated_at.isoformat(),
            'sentences': [
                {
                    'sentence': sentence.sentence,
                    'words': [
                        {
                            'word': word.word,
                            'head': word.head,
                            'relation': word.relation
                        }
                        for word in sentence.words
                    ]
                }
                for sentence in text.sentences
            ]
        }
    )
    try:
        with open(path.file_path, 'w', encoding='utf-8') as file:
            json.dump(res, file, ensure_ascii=False, indent=4)
        return {'message': f'File was saved to {path.file_path}!'}
    except Exception as e:
        return {'error': str(e)}
    
    return {'data': text}

@router.post("/texts/upload_file/{title}", tags=['Texts'])
def load_file(file_path: str, title: str):
    '''Загрузка файла с текстом, + название текста'''
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    parser = ParserFactory.get_parser(file_path)
    text = parser.parse(file_path)
    try:
        text_schema = TextSchema(content=text, title=title)
        processor = TextProcessor()
        sentences = processor.get_sentences(text)
        syntax_constructs = [
            {
            'words': processor.get_words(sent), 
            'sentence': sent,
            } 
            for sent in sentences
        ]
        insert_all_data(text=text_schema, syntax_constructs=syntax_constructs) 
    except Exception:
        raise HTTPException(status_code=409, detail='A text with this title already exists')
    return {'message': 'File was loaded successfully'}

@router.patch('/texts/new_content/{text_id}', tags=['Texts'])
def update_content(text_id: int, new_content: TextContentUpdateSchema):
    update_text_content(text_id=text_id, new_content=new_content.new_content)
    delete_sentences(text_id=text_id)
    processor = TextProcessor()
    sentences = processor.get_sentences(new_content.new_content)
    syntax_constructs = [
        {
        'words': processor.get_words(sent), 
        'sentence': sent,
        } 
        for sent in sentences
    ]
    insert_sentences(text_id=text_id, syntax_constructs=syntax_constructs)
    return {'message': f'Successfully update text with id {text_id}'}
