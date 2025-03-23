from pydantic import BaseModel


class SentenceSchema(BaseModel):
    text_id: int
    sentence: str
    
class SentenceGetSchema(BaseModel):
    id: int
    text_id: int
    sentence: str