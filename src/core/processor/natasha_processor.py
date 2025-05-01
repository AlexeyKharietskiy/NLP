import enum
from natasha import Segmenter, MorphVocab, NewsEmbedding, NewsSyntaxParser, Doc, NewsMorphTagger

from schemas.word_schemas import WordSchema

class TextProcessor:
    def __init__(self):
        self.segmenter = Segmenter()
        self.embedding = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(NewsEmbedding())
        self.syntax_parser = NewsSyntaxParser(self.embedding)
        
    def get_sentences(self, text) -> list[str]:
        doc = Doc(text)
        doc.segment(self.segmenter)

        result = []

        [result.append(sentence.text) for sentence in doc.sents]
        return result

    def get_words(self, sentence: str) -> list[WordSchema]:
        doc = Doc(sentence)
        doc.segment(self.segmenter)
        doc.parse_syntax(self.syntax_parser)
        
        result = []
        
        for token in doc.tokens:
            if hasattr(token, 'rel'):
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
    
processor = TextProcessor()