from typing import Optional
from sqlalchemy import and_, delete, func, select
from sqlalchemy.orm import aliased, selectinload
from src.database.database import session_factory, engine, Base
from src.models.texts_table import TextModel
from src.models.words_table import WordModel
from src.models.sentences_table import SentenceModel
from src.schemas.sentence_schemas import SentenceSchema
from src.schemas.text_schemas import TextSchema
from src.schemas.word_schemas import WordSchema

def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
def select_text_titles():
    with session_factory() as session:
        query = select(TextModel.id, TextModel.title)
        res = session.execute(query)
        titles = res.scalars().all
        return titles
    
def select_text(id: int):
    with session_factory() as session:
        res = session.get(TextModel, id)
        return res       
    
def select_sentences(text_id: int):
    with session_factory() as session:
        query = (
            select(SentenceModel).
            filter(SentenceModel.text_id == text_id)
        )
        res = session.execute(query)
        sentences = res.scalars().all()
        return sentences
    
def select_select_words(sent_id: int):
    with session_factory() as session:
        query = (
            select(WordModel).
            filter(TextModel.sentence_id == sent_id)
        )
        res = session.execute(query)
        words = res.scalars().all()
        return words
    
def select_all_text_info(id: int):
    with session_factory() as session:
        query = (
            select(TextModel)
            .where(TextModel.id==id)
            .options(
                selectinload(TextModel.sentences)
                .selectinload(SentenceModel.words)
                )
        )
        res = session.scalars(query).unique().first()
        return res
    
def insert_words(words: list[WordSchema], sentence_id : int):
    with session_factory() as session:
        word_models = [
            WordModel(
                word=word.word, 
                sentence_id= sentence_id,
                head=word.head_word,
                relation=word.relation
                ) 
            for word in words
            ]
        session.add_all(word_models)
        session.commit()
        
def insert_text(text: TextSchema):
    with session_factory() as session:
        text_model = TextModel(title=text.title, content=text.content)
        session.add(text_model)
        session.commit()
        
def insert_sentences(sentences: list[SentenceSchema], text_id: str):
    with session_factory() as session:
        sentence_models = [
            SentenceModel(
                sentence= sentence.sentence,
                text_id=text_id
            )
            for sentence in sentences
        ]
        session.add_all(sentence_models)
        session.commit()    
        
def select_words_by_rel(rel: str, sentence_id: int):
    with session_factory() as session:
        query = (
            select(WordModel)
            .where(
                and_(
                    WordModel.sentence_id == sentence_id,
                    WordModel.rel == rel
                    )
            )
        )
        res = session.scalars(query).unique().all()
        return res
    
def select_words_by_substr(substr: str, sentence_id: int):
    with session_factory() as session:
        query = (
            select(WordModel)
            .where(
                and_(
                    WordModel.sentence_id==sentence_id,
                    WordModel.word.contains(substr)
                )
            )
        )
        
        res = session.scalars(query).unique().all()
        return res
    
    
def update_text_content(new_content: str, text_id: int):
    with session_factory() as session:
        text = session.get(TextModel, text_id)
        text.content = new_content
        session.commit()