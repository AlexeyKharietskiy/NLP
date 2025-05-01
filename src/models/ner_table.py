from database.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.column_types import intpk


class NERModel(Base):
    __tablename__ = 'ners'
    
    id: Mapped[intpk]
    sentence_id: Mapped[int] = mapped_column(
        ForeignKey(
            'sentences.id',
            ondelete='CASCADE'
            )
        )
    ner: Mapped[str]
    type: Mapped[str]
    info: Mapped[str]
    
    sentence: Mapped['SentenceModel'] = relationship(
        back_populates='ners'
    )