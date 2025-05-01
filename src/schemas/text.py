from pydantic import BaseModel

class TextSchema(BaseModel):
    content: str
    title: str
    
class TextInsertSchema(BaseModel):
    file_path: str
    title: str