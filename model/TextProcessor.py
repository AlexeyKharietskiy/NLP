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
        self.morph_vocab = MorphVocab()  # Добавьте это для лемматизации

    def process_text(self):
        doc = Doc(self.text)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)

        word_forms = {}
        for token in doc.tokens:
            if token.pos not in {'PUNCT', 'SPACE'}:
                token.lemmatize(self.morph_vocab)
                word_form = token.text.lower()
                lemma = token.lemma
                if word_form not in word_forms:
                    word_forms[word_form] = WordForm(word_form, lemma, 0)
                word_forms[word_form].count += 1

        return list(word_forms.values())


# Пример использования
if __name__ == "__main__":
    text = "Привет, мир! Привет, друг. Мир добрый."
    text_processor = TextProcessor(text)
    word_forms = text_processor.process_text()
    for word_form in word_forms:
        print(word_form)