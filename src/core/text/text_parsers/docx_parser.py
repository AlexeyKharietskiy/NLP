from docx import Document

from core.text.text_parsers.file_parser import Parser

class DocxParser(Parser):
    def parse(self, file_path: str) -> str:
        doc = Document(file_path)
        return " ".join([paragraph.text for paragraph in doc.paragraphs])