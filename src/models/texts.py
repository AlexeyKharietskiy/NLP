
from sqlalchemy.orm import Mapped
from models.dependencies import create_at, updated_at, intpk
from database import Base


class TextModel(Base):
    __tablename__ = 'texts'
    
    id: Mapped[intpk]
    content: Mapped[str]  #=mapped_column() 
    title: Mapped[str]
    create_at: Mapped[create_at]
    updated_at: Mapped[updated_at]
