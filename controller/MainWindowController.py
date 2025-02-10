import tkinter
from view.MainView import MainView
from model.TextConverter import TextConverter
from logger import logger
from model.TextProcessor import TextProcessor


class MainWindowController:
    def __init__(self):
        self.window = None
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
            #открываем файлик
            text_converter = TextConverter(file)
            text = text_converter.convert_doc_docx_to_text()
            logger.info("File was opened")
            # натаха хуярит как не в себя
            text_processor = TextProcessor(text)
            self.word_form_list = text_processor.process_text()
            logger.info("Text has been processed")
            return self.fill_in_table()
        except Exception as e:
            #файлик оказался хуйней :(
            logger.error(f"File opening error: {e}")

    def fill_in_table(self):
        sorted_word_forms = sorted(self.word_form_list, key=lambda wf: wf.word_form.lower())
        table_data = [
            (wf.word_form, wf.lemma, wf.count, wf.morphological_info)  # Пустая строка для морфологической информации
            for wf in sorted_word_forms
        ]
        return table_data