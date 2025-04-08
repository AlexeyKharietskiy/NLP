from src.database.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.column_types import intpk

class SentenceModel(Base):
    __tablename__ = 'sentences'
    repr_cols_num = 3
    id: Mapped[intpk]
    text_id: Mapped[int] = mapped_column(ForeignKey('texts.id', ondelete='CASCADE'))
    sentence: Mapped[str]
    
    words: Mapped[list['WordModel']] = relationship(
        back_populates='sentence',
    )

    text: Mapped['TextModel'] = relationship(
        back_populates='sentences'
    )
