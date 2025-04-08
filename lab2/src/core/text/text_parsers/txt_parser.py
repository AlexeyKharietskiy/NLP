from core.text.text_parsers.file_parser import Parser


class TxtParser(Parser):
    def parse(self, file_path: str) -> str:
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read()
            return text.replace("\n", " ")