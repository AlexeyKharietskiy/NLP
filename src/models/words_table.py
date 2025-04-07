from src.database.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.column_types import intpk

class WordModel(Base):
    __tablename__ = 'words'
    repr_cols_num = 2
    id: Mapped[intpk]
    sentence_id: Mapped[int] = mapped_column(ForeignKey('sentences.id', ondelete='CASCADE'))
    word: Mapped[str]
    position: Mapped[int]
    sentence: Mapped['SentenceModel'] = relationship(
        back_populates='words'
    )
    sync_deps: Mapped[list['SynDepsModel']] = relationship(
        back_populates='words'
    )