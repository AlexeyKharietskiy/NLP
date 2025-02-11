import json
import os
from model.WordForm import WordForm
from logger import logger

#TODO как-то красиво все сделать
class JSONConverter:

    def __init__(self,file_path):
        self.file_path = file_path
        self.word_form_list = []

    def load_data_from_json(self, word_form_list=None):
        if not os.path.exists(self.file_path):
            self.word_form_list = word_form_list
        else:
            try:
                with open(self.file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.create_word_form_list(data)
            except json.JSONDecodeError:
                logger.error("Ошибка чтения JSON-файла.")

    def save_data_to_json(self, file_path):
        data = [word_form.to_dict() for word_form in self.word_form_list]
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            logger.info(f"Данные успешно сохранены в {file_path}")
        except Exception as e:
            logger.error(f"Ошибка записи в JSON-файл: {e}")

    def update_notes(self, data, word_form, morphological_info):
        """
        Обновляет заметки для указанной словоформы в данных.
        """
        for entry in self.word_form_list:
            if entry.word_form == word_form:
                entry.morphological_info = morphological_info
                logger.info(f"Заметки для '{word_form}' обновлены: {morphological_info}")
                return True
        logger.error(f"Словоформа '{word_form}' не найдена.")
        return False

    def create_word_form_list(self, data):
        self.word_form_list = [
            WordForm(
                item.get("word_form", ""),
                item.get("lemma", ""),
                item.get("count", 0),
                item.get("morphological_info", "")
            ) for item in data
        ]



def main():
    # Путь к JSON-файлу
    json_file = "test.json"
    converter = JSONConverter(json_file)
    data = converter.load_data_from_json()
    converter.update_notes(data,"и", "хуй")
    converter.save_data_to_json(json_file)
if __name__ == "__main__":
    main()