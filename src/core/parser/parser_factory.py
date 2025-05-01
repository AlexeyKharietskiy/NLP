
import os

from core.parser.parser import Parser
from core.parser.docx_parser import DocxParser
from core.parser.pdf_parser import PdfParser
from core.parser.txt_parser import TxtParser


class ParserFactory:
    '''
    Factory for creating different file format parsers 
    '''
    FORMATS = {
        ".txt": TxtParser,
        ".docx": DocxParser,
        ".pdf": PdfParser,
    }
    @staticmethod
    def get_parser(file_path: str) -> Parser:
        file_name, file_extension = os.path.splitext(file_path)
        if file_extension in ParserFactory.FORMATS.keys():
            return ParserFactory.FORMATS[file_extension]()  
        else:
            raise ValueError(f"Unsupported file type: {file_path}")