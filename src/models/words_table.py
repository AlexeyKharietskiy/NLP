from database.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.column_types import intpk

class WordModel(Base):
    __tablename__ = 'words'
    repr_cols_num = 2
    id: Mapped[intpk]
    sentence_id: Mapped[int] = mapped_column(ForeignKey('sentences.id', ondelete='CASCADE'))
    word: Mapped[str]
    head: Mapped[str]
    relation: Mapped[str]
    
    sentence: Mapped['SentenceModel'] = relationship(
        back_populates='words'
    )