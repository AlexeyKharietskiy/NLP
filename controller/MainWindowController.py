import tkinter
from view.MainView import MainView
from model.TextConverter import TextConverter
from logger import logger
from model.TextProcessor import TextProcessor

#TODO сохранение морфологической информации
#TODO реализация поиска
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
            return self.fill_in_table(self.word_form_list)
        except Exception as e:
            #файлик оказался хуйней :(
            logger.error(f"File opening error: {e}")

    @staticmethod
    def fill_in_table(word_list):
        sorted_word_forms = sorted(word_list, key=lambda wf: wf.word_form.lower())
        table_data = [
            (wf.word_form, wf.lemma, wf.count, wf.morphological_info)  # Пустая строка для морфологической информации
            for wf in sorted_word_forms
        ]
        return table_data

    def search_words(self, text):
        query = text.strip().lower()
        if not query:
            return self.fill_in_table(self.word_form_list)

        filtered_data = [row for row in self.word_form_list if query in str(row.word_form).lower()]
        return self.fill_in_table(filtered_data)

