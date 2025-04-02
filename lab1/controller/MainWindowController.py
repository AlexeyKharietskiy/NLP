import tkinter
from view.MainView import MainView
from model.TextConverter import TextConverter
from lab1.logger import logger
from model.TextProcessor import TextProcessor
from model.JSONConverter import JSONConverter

class MainWindowController:
    def __init__(self):
        self.window = None
        self.json_converter = None
        self.word_form_list = []
        self.current_file_path = None

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
            self.current_file_path = file
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
        self.save_data_to_json()

    def read_json_file(self, path):
        json_path = self.create_json_path(path)
        self.json_converter = JSONConverter(json_path)
        return self.json_converter.load_data_from_json()

    def save_data_to_json(self):
        if self.current_file_path:
            json_path = self.create_json_path(self.current_file_path)
            self.json_converter = JSONConverter(json_path)
            self.json_converter.set_word_form_list(self.word_form_list)
            self.json_converter.save_data_to_json()

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

    def update_word_form_morphological_info(self, word_form, new_info):
        for wf in self.word_form_list:
            if wf.word_form == word_form:
                wf.morphological_info = new_info
                logger.info(f"Morphological information for '{wf.word_form}' was updated: '{wf.morphological_info}'")
                break
        self.save_data_to_json()