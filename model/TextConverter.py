import win32com.client

class TextConverter:
    def __init__(self, file_path):
        self.file_path = file_path

    def convert_doc_docx_to_text(self):
        try:
            word = win32com.client.Dispatch("Word.Application")
            word.Visible = False
            doc = word.Documents.Open(self.file_path)
            text = doc.Range().Text
            doc.Close(False)
            word.Quit()
            return text
        except Exception as e:
            raise Exception(f"Read file error: {e}")