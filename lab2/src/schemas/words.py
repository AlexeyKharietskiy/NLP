from pydantic import BaseModel


class WordSchema(BaseModel):
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