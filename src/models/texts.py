from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.dependencies import create_at, updated_at, intpk
from database import Base


class TextModel(Base):
    __tablename__ = 'texts'
    repr_cols_num = 2
    
    id: Mapped[intpk]
    title: Mapped[str] = mapped_column(unique=True,)
    content: Mapped[str] 
    create_at: Mapped[create_at]
    updated_at: Mapped[updated_at]
    words: Mapped[list['WordModel']] = relationship(
        back_populates='text'
    )
    