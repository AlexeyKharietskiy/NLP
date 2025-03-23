from pydantic import BaseModel


class WordSchema(BaseModel):
    sentence_id: int
    lemma: str
    word: str
    part_of_speech: str
    feats: dict
    
class WordGetSchema(BaseModel):
    id: int
    sentence_id: int
    lemma: str
    word: str
    part_of_speech: str
    feats: dict