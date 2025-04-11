from pydantic import BaseModel

class TextSchema(BaseModel):
    content: str
    title: str
    
class TextContentUpdateSchema(BaseModel):
    new_content: str
    
class FilePathSchema(BaseModel):
    file_path: str
    
class TextInsertSchema(BaseModel):
    file_path: str
    title: str