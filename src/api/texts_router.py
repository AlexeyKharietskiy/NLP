from typing import Annotated
from fastapi import APIRouter, Body, HTTPException
import os

from core.parser.parser_factory import ParserFactory
from core.processor.processor import TextProcessor
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
from schemas.text import (
    TextInsertSchema, 
)

router = APIRouter()

@router.get("/texts/text_titles", tags=['Texts'])
def get_texts_titles():
    """Get all titles and ides

    Raises:
        HTTPException: do not have any titles

    Returns:
        data: [
            id: int,
            title: str
        ]
    """
    text_titles = select_text_titles()
    if not text_titles:
        raise HTTPException(status_code=404, detail=f'Do not find text titles')
    return {'data': text_titles}

@router.get('/texts/concrete_text/{text_id}', tags=['Texts'])
def get_text(text_id: int):
    """Get all text data

    Args:
        text_id (int): selected text id from database

    Raises:
        HTTPException: do not find text with such id

    Returns:
        data: 
            id: int, 
            title: str, 
            content: str,
            created_at: datetime, 
            updated_at: datetime
        
    """
    text = select_text(text_id)
    if not text:
        raise HTTPException(status_code=404, detail=f'Do not find text with such ID: {text_id}')
    return {'data': text}

@router.post('/texts/save/{text_id}', tags=['Texts'])
def get_all_text_info(text_id: int, filepath: Annotated[str, Body()]):
    """Save processed text date into json file:

    Args:
        text_id (int): text id from database
        path (Annotated[str, Body()]): filepath

    Raises:
        HTTPException: do not find filepath
        HTTPException: do not find text data

    Returns:
        data: dict
    """
    if not filepath:
        raise HTTPException(status_code=404, detail=f"Do not find file: {filepath}")
    text = select_all_text_info(text_id)
    if not text:
        raise HTTPException(
            status_code=404, 
            detail=f'Do not find info of the text with such ID: {text_id}'
            )
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
    # with open(filepath, 'w', encoding='utf-8') as file:
    #     json.dump(res, file, ensure_ascii=False, indent=4)
    return {'data': res}

@router.post("/texts/upload_file", tags=['Texts'])
def load_file(text_data: TextInsertSchema):
    create_tables()
    """Process text from file and loaded it into database

    Args:
        text_data (TextInsertSchema): text title and file_path

    Raises:
        HTTPException: if do not find filepath (404)
        HTTPException: if title is not unique (409)

    Returns:
        message: str
    """
    if not os.path.exists(text_data.file_path):
        raise HTTPException(status_code=404, detail="File not found")
    parser = ParserFactory.get_parser(text_data.file_path)
    text = parser.parse(text_data.file_path)
    # try:
    text_params = {
        'content': text, 
        "title": text_data.title
        }
    processor = TextProcessor()        
    result = processor.process(text)
    syntax_constructs = [
        {
        'words': sent['words'], 
        'ners': sent['ners'], 
        'sentence': sent['sentence'],
        } 
        for sent in result['sentences']
    ]
    insert_all_data(text_params=text_params, sentences=syntax_constructs) 
    # except Exception:
    #     raise HTTPException(status_code=409, detail='A text with this title already exists')
    return {'message': 'File was loaded successfully'}

@router.patch('/texts/new_content/{text_id}', tags=['Texts'])
def update_content(text_id: int, new_content: Annotated[str, Body()]):
    """Update all text data by new content

    Args:
        text_id (int): Selected text id from database
        new_content (TextContentUpdateSchema): pydantic schema with field 'new_content: str'

    Raises:
        HTTPException: Do not find this text

    Returns:
        message: str
    """
    try:
        update_text_content(text_id=text_id, new_content=new_content)
        delete_sentences(text_id=text_id)
        sentences = processor.get_sentences(new_content)
        syntax_constructs = [
            {
            'words': processor.get_words(sent), 
            'sentence': sent,
            } 
            for sent in sentences
        ]
        insert_sentences(text_id=text_id, syntax_constructs=syntax_constructs)
    except AttributeError:
        raise HTTPException(status_code=404, detail=f'Do not find text with id {text_id}')
    return {'message': f'Successfully update text with id {text_id}'}
