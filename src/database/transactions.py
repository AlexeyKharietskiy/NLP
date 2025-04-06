from typing import Optional
from sqlalchemy import and_, delete, func, select
from sqlalchemy.orm import aliased
from src.database.database import session_factory, engine, Base
from src.models.texts_table import TextModel
from src.models.words_table import WordModel
from src.models.sentences_table import SentenceModel
from src.models.syntax_deps_table import SynDepsModel

def create_tables():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
        