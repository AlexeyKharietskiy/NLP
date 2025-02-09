from view.MainView import MainView
from model.TextConverter import TextConverter
from logger import logger
from model.TextProcessor import TextProcessor

class MainWindowController:
    def __init__(self):
        self.window = None
        self.text_processor = None

    def open_window(self):
        if self.window is not None and self.window.winfo_exists():
            self.window.destroy()
        self.window = MainView(self)
        self.window.main()


    def open_file(self, file):
        try:
            text_converter = TextConverter(file)
            text = text_converter.convert_doc_docx_to_text()
            logger.info("File was opened")
            self.text_processor = TextProcessor(text)
            logger.info("Text has been processed")
        except Exception as e:
            logger.error(f"File opening error: {e}")

