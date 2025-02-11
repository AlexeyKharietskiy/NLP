from natasha import (
    Segmenter,
    NewsEmbedding,
    NewsMorphTagger,
    MorphVocab,
    Doc
)
from model.WordForm import WordForm

class TextProcessor:
    def __init__(self, text):
        self.text = text
        self.segmenter = Segmenter()
        self.emb = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.morph_vocab = MorphVocab()

    @staticmethod
    def is_russian_word(token):
        if token.pos in {'PUNCT', 'SPACE'}:
            return False

        text = token.text.lower()

        if all(
                ('а' <= c <= 'я' or c == 'ё')
                or c in "-'"
                for c in text
        ) and any(c.isalpha() for c in text):
            return True

        return False

    def process_text(self):
        doc = Doc(self.text)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)

        word_form_list = {}
        for token in doc.tokens:
            if self.is_russian_word(token):  # Проверяем, является ли слово русским
                token.lemmatize(self.morph_vocab)
                word_form = token.text.lower()
                lemma = token.lemma
                if word_form not in word_form_list:
                    word_form_list[word_form] = WordForm(word_form, lemma, 0)
                word_form_list[word_form].count += 1

        return list(word_form_list.values())