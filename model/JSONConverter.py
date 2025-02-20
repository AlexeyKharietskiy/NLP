import json
import os
from model.WordForm import WordForm
from logger import logger

class JSONConverter:
    def __init__(self, file_path):
        self.file_path = file_path
        self.word_form_list = []

    def load_data_from_json(self, default_word_form_list=None):

        if not os.path.exists(self.file_path):
            logger.info(f"Didn't find file {self.file_path}.")
            self.word_form_list = default_word_form_list or []
            return self.word_form_list

        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                logger.info(f"Successfully uploaded data from {self.file_path}")
                self.create_word_form_list(data)
                return self.word_form_list
        except json.JSONDecodeError:
            logger.error("Read JSON-file error")
            return []

    def save_data_to_json(self):
        if not self.file_path:
            return

        try:
            data = [word_form.to_dict() for word_form in self.word_form_list]
            with open(self.file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            logger.info(f"Successfully loaded data in {self.file_path}")
        except Exception as e:
            logger.error(f"Write error JSON-file: {e}")

    def create_word_form_list(self, data):
        self.word_form_list = [
            WordForm(
                item.get("word_form", ""),
                item.get("lemma", ""),
                item.get("count", 0),
                item.get("morphological_info", "")
            ) for item in data
        ]

    def set_word_form_list(self, word_form_list):
        self.word_form_list = word_form_list
