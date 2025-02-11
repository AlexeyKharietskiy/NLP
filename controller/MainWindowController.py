import tkinter
from view.MainView import MainView
from model.TextConverter import TextConverter
from logger import logger
from model.TextProcessor import TextProcessor
from model.JSONConverter import JSONConverter

#TODO сохранение морфологической информации в json
class MainWindowController:
    def __init__(self):
        self.window = None
        self.json_converter = None
        self.word_form_list = []

    def open_window(self):
        if self.window is not None:
            try:
                if self.window.winfo_exists():
                    self.window.destroy()
            except tkinter.TclError:
                pass
        self.window = MainView(self)
        self.window.main()

    def open_file(self, file):
        try:
            self.word_form_list = self.read_json_file(file)
            if not self.word_form_list:
                self.process_file(file)
            return self.fill_in_table(self.word_form_list)
        except Exception as e:
            logger.error(f"File opening error: {e}")


    def process_file(self, file):
        text_converter = TextConverter(file)
        text = text_converter.convert_doc_docx_to_text()
        logger.info(f"File {file} was opened")
        text_processor = TextProcessor(text)
        self.word_form_list = text_processor.process_text()
        logger.info("Text has been successfully processed")

    def read_json_file(self, path):
        json_path = self.create_json_path(path)
        self.json_converter = JSONConverter(json_path)
        return self.json_converter.load_data_from_json(self.word_form_list)

    @staticmethod
    def fill_in_table(word_list):
        sorted_word_forms = sorted(word_list, key=lambda wf: wf.word_form.lower())
        table_data = [
            (wf.word_form, wf.lemma, wf.count, wf.morphological_info)
            for wf in sorted_word_forms
        ]
        return table_data

    def search_words(self, text):
        query = text.strip().lower()
        if not query:
            return self.fill_in_table(self.word_form_list)
        filtered_data = [row for row in self.word_form_list if query in str(row.word_form).lower()]
        return self.fill_in_table(filtered_data)

    @staticmethod
    def create_json_path(path):
        if path.lower().endswith(('.doc', '.docx')):
            base_name = path.rsplit('.', 1)[0]
            return f"{base_name}.json"
        else:
            return f"{path}.json"

