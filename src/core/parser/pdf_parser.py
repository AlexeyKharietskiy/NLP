import fitz
from core.parser.parser import Parser
from log import logger

class PdfParser(Parser):
    def parse(self, file_path: str) -> str:
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
                
        logger.info('Parse PDF file')
        return text.replace("\n", " ")