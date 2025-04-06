from src.database.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.column_types import intpk

class SynDepsModel(Base):
    __tablename__ = 'syn_deps'
    repr_cols_num = 4
    id: Mapped[intpk]
    word_id: Mapped[int] = mapped_column(ForeignKey('words.id', ondelete='CASCADE'))
    head_id: Mapped[int] = mapped_column(ForeignKey('words.id', ondelete='CASCADE'))
    relation: Mapped[str]