import datetime
from pydantic import BaseModel


class TextSchema(BaseModel):
    content: str
    author: str
    title: str
    create_at: datetime.datetime
    update_at: datetime.datetime
    
class TextGetSchema(BaseModel):
    id: int
    content: str
    author: str
    title: str
    create_at: datetime.datetime
    update_at: datetime.datetime