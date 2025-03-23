
from database import sync_engine, sync_session_factory, Base
from models.sentences import SentenceModel
from models.texts import TextModel
from models.words import WordModel

def create_tables():
    sync_engine.echo = False
    Base.metadata.drop_all(sync_engine)
    sync_engine.echo = True
    Base.metadata.create_all(sync_engine)
    
# def insert_words(words: list):
#     with sync_session_factory() as session:
#         tokens =[]
#         for word in words:
#             tokens.append(WordModel(
#                 lemma=word.lemma,
#                 word=word.word,
#                 part_of_speech = word.part_of_speech,
#                 feats = word.part_of_speech
#                 ))
#             session.add_all(tokens)
#     session.commit
    