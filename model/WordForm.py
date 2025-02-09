class WordForm:
    def __init__(self, word_form, lemma, count):
        self.word_form = word_form
        self.lemma = lemma
        self.count = count

    def __repr__(self):
        return f"WordForm(word_form='{self.word_form}', lemma='{self.lemma}', count={self.count})"