from models.dependencies import intpk
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class SentenceModel(Base):
    __tablename__ = 'sentences'
    
    id: Mapped[intpk]
    text_id: Mapped[int] = mapped_column(ForeignKey("texts.id", ondelete="CASCADE")) 
    sentence: Mapped[str]
