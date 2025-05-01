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
    
    