class WordForm:
    def __init__(self, word_form, lemma, count, morphological_info=""):
        self.word_form = word_form
        self.lemma = lemma
        self.count = count
        self.morphological_info = morphological_info

    def to_dict(self):
        """
        Преобразует объект WordForm в словарь для записи в JSON.
        """
        return {
            "word_form": self.word_form,
            "lemma": self.lemma,
            "count": self.count,
            "morphological_info": self.morphological_info
        }