from typing import Optional
from sqlalchemy import and_, delete, func, select
from sqlalchemy.orm import aliased, selectinload
from database.database import session_factory, engine, Base
from models.texts_table import TextModel
from models.words_table import WordModel
from models.sentences_table import SentenceModel
from models.ner_table import NERModel
from log import logger

def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    engine.echo = True
    logger.info('Recreate DB')
    
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

def select_syntax_words(sent_id: int):
    with session_factory() as session:
        query = select(
            WordModel.id, 
            WordModel.word,
            WordModel.head,
            WordModel.relation
            ).filter(WordModel.sentence_id == sent_id)
        res = session.execute(query)
        return [
            {
                "id": row[0], 
                "word": row[1],
                "head": row[2],
                "relation": row[3]
                } 
            for row in res
            ]
    
def select_morphological_words(sent_id: int):
    with session_factory() as session:
        query = select(
            WordModel.id, 
            WordModel.word,
            WordModel.pos,
            WordModel.feats
            ).filter(WordModel.sentence_id == sent_id)
        res = session.execute(query)
        return [
            {
                "id": row[0], 
                "word": row[1],
                "pos": row[2],
                "feats": row[3]
                } 
            for row in res
            ]

def select_ners(sent_id: int):
    with session_factory() as session:
        query = (
            select(NERModel).
            filter(NERModel.sentence_id == sent_id)
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
    
def insert_words(words: list[dict], sentence_id : int):
    with session_factory() as session:
        word_models = [
            WordModel(
                word=word['word'], 
                sentence_id=sentence_id,
                head=word['head_word'],
                relation=word['relation'],
                pos = word['pos'],
                feats = word['feats']
                ) 
            for word in words
            ]
        session.add_all(word_models)
        session.commit()
        
def insert_all_data(text_params: dict, sentences: list[dict]):
    with session_factory() as session:
        text_model = TextModel(
            title=text_params['title'], 
            content=text_params['content']
            )
        session.add(text_model)
        session.flush()
        for sentence in sentences:
            sent = SentenceModel(
                sentence=sentence['sentence'], 
                text_id=text_model.id
                )
            session.add(sent)
            session.flush()
            word_models = []
            ner_models = []
            for word in sentence['words']:
                word_models.append(
                    WordModel(
                        word=word['word'], 
                        sentence_id=sent.id,
                        head=word['head_word'],
                        relation=word['relation'],
                        pos = word['pos'],
                        feats = word['feats']
                    ))
                
            for ner in sentence['ners']:
                ner_models.append(
                    NERModel(
                        ner=ner['ner'], 
                        sentence_id=sent.id,
                        type=ner['type'],
                    ))  
            session.add_all(word_models)
            session.add_all(ner_models)
        session.commit()
        
def insert_sentences(sentences: list[dict], text_id: str):
    with session_factory() as session:
        for sentence in sentences:
            sent = SentenceModel(sentence=sentence['sentence'], text_id=text_id)
            session.add(sent)
            session.flush()
            word_models = []
            ner_models = []
            for word in sentence['words']:
                word_models.append(
                    WordModel(
                        word=word['word'], 
                        sentence_id=sent.id,
                        head=word['head_word'],
                        relation=word['relation'],
                        pos = word['pos'],
                        feats = word['feats']
                    )) 
                
            for ner in sentence['ners']:
                ner_models.append(
                    NERModel(
                        ner=ner['ner'], 
                        sentence_id=sent.id,
                        type=ner['type'],
                    ))  
            session.add_all(word_models)
            session.add_all(ner_models)        
        session.commit()
        
def select_words_by_pos(pos: str, sentence_id: int):
    with session_factory() as session:
        query = (
            select(WordModel)
            .where(
                and_(
                    WordModel.sentence_id == sentence_id,
                    WordModel.pos == pos
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