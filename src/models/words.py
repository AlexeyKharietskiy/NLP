from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.dependencies import intpk
from database import Base
    
class WordModel(Base):
    __tablename__ = 'words'
    id: Mapped[intpk]
    text_id: Mapped[int] = mapped_column(ForeignKey("texts.id", ondelete="CASCADE"))
    word: Mapped[str]
    frequency: Mapped[int]
    lemma: Mapped[str] 
    part_of_speech: Mapped[str]
    feats: Mapped[str]
    
    text: Mapped['TextModel'] = relationship(
        back_populates='words'
    )
    
