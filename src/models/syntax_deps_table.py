from src.database.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.column_types import intpk

class SynDepsModel(Base):
    __tablename__ = 'syn_deps'
    repr_cols_num = 4
    id: Mapped[intpk]
    word_id: Mapped[int] = mapped_column(ForeignKey('words.id', ondelete='CASCADE'))
    head_id: Mapped[int] = mapped_column(
        ForeignKey('words.id', ondelete='CASCADE'),
        nullable=True
        )
    relation: Mapped[str]
    words: Mapped[list['WordModel']] = relationship(
        back_populates='syn_deps',
        foreign_keys=[word_id]
    )
    heads: Mapped[list['WordModel']] = relationship(
        back_populates='syn_deps',
        foreign_keys=[head_id]
    )