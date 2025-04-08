from pydantic import BaseModel

class WordSchema(BaseModel):
    word: str
    head_word: str
    relation: str