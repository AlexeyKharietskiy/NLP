from typing import Optional
from sqlalchemy import and_, delete, func, select
from sqlalchemy.orm import selectinload
from database import sync_session_factory, sync_engine, Base
from models.texts import TextModel
from models.words import WordModel
from schemas.texts import TextSchema
from schemas.words import WordSchema


def create_tables():
    sync_engine.echo = False
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
    sync_engine.echo = True
    
def insert_text(text: TextSchema) -> TextModel:
    with sync_session_factory() as session:
        text_row = TextModel(content=text.content, title=text.title)
        session.add(text_row)
        session.flush()
        session.commit()
        return text_row.id        
        
def insert_words(words: list[WordSchema], text_id: int):
    with sync_session_factory() as session:
        for word in words:
            word_row = WordModel(
                word=word.word, 
                lemma=word.lemma, 
                text_id=text_id, 
                frequency=word.frequency,
                part_of_speech=word.part_of_speech, 
                feats=word.feats
                )
            session.add(word_row)
        session.flush()
        session.commit()
        
def select_texts():
    with sync_session_factory() as session:
        query = select(TextModel)
        result = session.execute(query)
        texts = result.scalars().all()
        return texts

def select_text_by_id(text_id: int):
    with sync_session_factory() as session:
        query = (
            select(TextModel)
            .filter(TextModel.id==text_id)
            )
        result = session.execute(query)
        text = result.scalars().first()
        return text

def select_words_from_text(text_id: int):
    with sync_session_factory() as session:
        query = (
            select(WordModel)
            .filter(WordModel.text_id==text_id)
            )
        result = session.execute(query)
        words = result.scalars().all()
        return words
    
def select_word_by_pos(pos: str, text_id: int):
    with sync_session_factory() as session:
        query = (
            select(WordModel)
            .filter(and_(
                WordModel.part_of_speech==pos,
                WordModel.text_id==text_id
                ))
            )
        result = session.execute(query)
        words = result.scalars().all()
        return words
    
def select_words_by_content(text_id: int, content: str):
    with sync_session_factory() as session:
        query = (
            select(WordModel)
            .where(and_(
                WordModel.word.contains(content),
                WordModel.text_id==text_id
                ))
            )
        result = session.execute(query)
        words = result.scalars().all()
        if not words:
            raise ValueError(f"No words found containing '{content}' for text_id {text_id}")
        return words
            
def delete_text_by_id(text_id: int):
    with sync_session_factory() as session:
        text = session.get(TextModel, text_id)
        if text: 
            session.delete(text)
            session.commit()
        else:
            session.rollback()
            raise ValueError(f'No record with such id: {text_id}')
        
def update_text_values(text_id: int, new_content:Optional[str], new_title:Optional[str]):
    with sync_session_factory() as session:
        text = session.get(TextModel, text_id)
        if not text:
            raise ValueError(f'No record with such id: {text_id}')
        if new_content:
            text.content = new_content
        if new_title:
            text.title=new_title
        query = (delete(WordModel)
                 .filter(WordModel.text_id==text_id))
        session.execute(query)
        session.commit()
        
def select_all_data() -> list[TextModel]:
    with sync_session_factory() as session:
        query = (
            select(TextModel).
            options(
                selectinload(TextModel.words)
            )
        )
        res = session.scalars(query).unique().all()
        return res