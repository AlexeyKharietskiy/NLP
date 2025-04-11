from typing import Optional
from sqlalchemy import and_, delete, func, select
from sqlalchemy.orm import aliased, selectinload
from database.database import session_factory, engine, Base
from models.texts_table import TextModel
from models.words_table import WordModel
from models.sentences_table import SentenceModel
from schemas.sentence_schemas import SentenceSchema
from schemas.text_schemas import TextSchema
from schemas.word_schemas import WordSchema

def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    engine.echo = True
    
    
def select_text_titles():
    with session_factory() as session:
        query = select(TextModel.id, TextModel.title)
        res = session.execute(query)
        return [{"id": row[0], "title": row[1]} for row in res]
    
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
    
def select_words(sent_id: int):
    with session_factory() as session:
        query = (
            select(WordModel).
            filter(WordModel.sentence_id == sent_id)
        )
        res = session.execute(query)
        words = res.scalars().all()
        return words
    
def select_all_text_info(id: int) -> TextModel:
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
                sentence_id=sentence_id,
                head=word.head_word,
                relation=word.relation
                ) 
            for word in words
            ]
        session.add_all(word_models)
        session.commit()
        
def insert_all_data(text: TextSchema, syntax_constructs: list[dict]):
    with session_factory() as session:
        text_model = TextModel(title=text.title, content=text.content)
        session.add(text_model)
        session.flush()
        for syntax_construct in syntax_constructs:
            sent = SentenceModel(sentence=syntax_construct['sentence'], text_id=text_model.id)
            session.add(sent)
            session.flush()
            word_models=[]
            for words_schema in syntax_construct['words']:
                word_models.append(
                    WordModel(
                        word=words_schema.word,
                        head=words_schema.head_word, 
                        relation=words_schema.relation, 
                        sentence_id=sent.id,
                    )) 
                    
                session.add_all(word_models)
                session.flush()
        session.commit()
        
def insert_sentences(syntax_constructs: list[dict], text_id: str):
    with session_factory() as session:
        for syntax_construct in syntax_constructs:
            sent = SentenceModel(sentence=syntax_construct['sentence'], text_id=text_id)
            session.add(sent)
            session.flush()
            word_models=[]
            for words_schema in syntax_construct['words']:
                word_models.append(
                    WordModel(
                        word=words_schema.word,
                        head=words_schema.head_word, 
                        relation=words_schema.relation, 
                        sentence_id=sent.id,
                    )) 
                    
                session.add_all(word_models)
                session.flush()
        session.commit()
        
def select_words_by_rel(rel: str, sentence_id: int):
    with session_factory() as session:
        query = (
            select(WordModel)
            .where(
                and_(
                    WordModel.sentence_id == sentence_id,
                    WordModel.relation == rel
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
    engine.echo = True
    with session_factory() as session:
        text = session.get(TextModel, text_id)
        text.content = new_content
        session.commit()
        
def delete_sentences(text_id: int):
    with session_factory() as session:
        query = (
            delete(SentenceModel)
            .where(SentenceModel.text_id==text_id)
        )
        session.execute(query)
        session.commit()