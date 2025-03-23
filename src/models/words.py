import enum
from sqlalchemy import ForeignKey
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
class WordPos(enum.Enum):
    NOUN = "имя существительное"
    ADJ = "имя прилагательное"
    VERB = "глагол"
    INFN = "инфинитив"
    PRTF = "причастие"
    PRTS = "деепричастие"
    NUMR = "числительное"
    ADV = "наречие"
    NPRO = "местоимение"
    PRED = "предикатив"
    PREP = "предлог"
    CONJ = "союз"
    PRCL = "частица"
    INTJ = "междометие"
    
class WordModel(Base):
    __tablename__ = 'words'
    
    id: Mapped[intpk]
    sentence_id: Mapped[int] = mapped_column(ForeignKey("sentences.id", ondelete="CASCADE"))
    lemma: Mapped[str]  #=mapped_column() 
    word: Mapped[str]
    part_of_speech: Mapped[WordPos]
    feats: Mapped[str]
