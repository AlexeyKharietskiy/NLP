import fitz
from src.core.parser.parser import Parser


class PdfParser(Parser):
    def parse(self, file_path: str) -> str:
        text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()
        return text