from docx import Document


class TextConverter:
    def __init__(self, file_path):
        self.file_path = file_path

    def convert_doc_docx_to_text(self):
        doc = Document(self.file_path)
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        return '\n'.join(full_text)
