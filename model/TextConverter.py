import win32com.client

class TextConverter:
    def __init__(self, file_path):
        self.file_path = file_path

    def convert_doc_docx_to_text(self):
        try:
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False  # Скрываем окно Word
            doc = word.Documents.Open(self.file_path)
            text = doc.Range().Text  # Получаем весь текст
            doc.Close(False)  # Закрываем документ без сохранения
            word.Quit()  # Закрываем приложение Word
            return text
        except Exception as e:
            raise Exception(f"Ошибка при чтении файла: {e}")