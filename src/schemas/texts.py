import datetime
from typing import Optional
from pydantic import BaseModel


class TextSchema(BaseModel):
    content: str
    title: str
    
class TextGetSchema(BaseModel):
    id: int
    content: str
    title: str
    
class FilePathSchema(BaseModel):
    file_path: str