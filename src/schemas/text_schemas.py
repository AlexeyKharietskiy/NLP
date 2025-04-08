from pydantic import BaseModel

class TextSchema(BaseModel):
    content: str
    title: str