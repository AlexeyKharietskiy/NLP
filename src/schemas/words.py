from pydantic import BaseModel


class WordSchema(BaseModel):
    # text_id: int
    lemma: str
    word: str
    part_of_speech: str
    frequency: int
    feats: str
    def __eq__(self, other):
        if not isinstance(other, WordSchema):
            return False
        return self.word == other.word and\
            self.part_of_speech == other.part_of_speech and\
            self.feats == other.feats
    
class WordGetSchema(BaseModel):
    id: int
    text_id: int
    lemma: str
    word: str
    frequency: int
    part_of_speech: str
    feats: str