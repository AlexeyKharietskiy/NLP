from pydantic import BaseModel

class SentenceSchema(BaseModel):
    sentence: str
