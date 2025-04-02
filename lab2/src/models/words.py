import enum
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column
from models.dependencies import intpk
from database import Base
# data = {'pos': 'NOUN'}

# # Получаем значение из словаря
# pos_key = data['pos']

# # Получаем элемент перечисления по имени
# pos_enum = WordPos[pos_key]

# # Получаем строковое значение
# pos_value = pos_enum.value

# print(pos_value)  # Output: "имя существительное"
    
class WordModel(Base):
    __tablename__ = 'words'
    id: Mapped[intpk]
    text_id: Mapped[int] = mapped_column(ForeignKey("texts.id", ondelete="CASCADE"))
    word: Mapped[str]
    frequency: Mapped[int]
    lemma: Mapped[str] 
    part_of_speech: Mapped[str]
    feats: Mapped[str]
