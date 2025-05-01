from log import logger
from docx import Document
from core.parser.parser import Parser


class DocxParser(Parser):
    def parse(self, file_path: str) -> str:
        doc = Document(file_path)
        logger.info('Parse DOCX file')
        return " ".join([paragraph.text for paragraph in doc.paragraphs])