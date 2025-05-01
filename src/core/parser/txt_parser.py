from core.parser.parser import Parser
from log import logger


class TxtParser(Parser):
    def parse(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            logger.info('Parse TXT file')
            return text.replace("\n", " ")