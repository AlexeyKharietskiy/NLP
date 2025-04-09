from natasha import Segmenter, MorphVocab, NewsEmbedding, NewsSyntaxParser, Doc, NewsMorphTagger

from src.schemas.word_schemas import WordSchema

class TextProcessor:
    def __init__(self):
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        self.embedding = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(NewsEmbedding())
        self.syntax_parser = NewsSyntaxParser(self.embedding)
        
    def get_sentences(self, text):
        doc = Doc(text)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)

        # Формируем структуру данных
        result = []

        for sentence in doc.sents:
            sentence_text = sentence.text
            result.append(sentence_text)
        return result

    def get_words(self, sentence: str) -> list[WordSchema]:
        doc = Doc(sentence)
        doc.segment(self.segmenter)  # Сегментация на предложения
        doc.tag_morph(self.morph_tagger)  # Морфологический разбор
        doc.parse_syntax(self.syntax_parser)  # Синтаксический разбор
        
        result = []
        
        # Правильный перебор токенов
        for token in doc.tokens:  # Используем doc.tokens вместо sent
            if hasattr(token, 'pos') and token.pos in {
                "NOUN", "VERB", "ADJ", "NUMR",
                "ADV", "PRON", "PROPN", "PART", 
                "CCONJ", "SCONJ", "ADP", "DET",
                "INFN", 'PRTF', 'PRTS', 'PRED',
                'INTJ'
            }:
                # Находим головное слово
                head_word = next(
                    (t.text for t in doc.tokens if t.id == token.head_id),
                    ''
                )
                
                result.append(
                    WordSchema(
                        word=token.text,
                        head_word=head_word,
                        relation=token.rel
                    )
                )
        
        return result