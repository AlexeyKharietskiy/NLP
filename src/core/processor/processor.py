from natasha import (
    MorphVocab,
    Segmenter, 
    NewsEmbedding, 
    NewsSyntaxParser, 
    Doc,
    NewsMorphTagger,
    NewsNERTagger
    )
from log import logger

class TextProcessor:
    def __init__(self):
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        self.embedding = NewsEmbedding()
        self.morph_tagger = NewsMorphTagger(NewsEmbedding())
        self.syntax_parser = NewsSyntaxParser(self.embedding)
        self.ner_tagger = NewsNERTagger(self.embedding)
        
    def process(self, text: str) -> dict:
        doc = Doc(text)
        doc.segment(self.segmenter)

        result = {
            'text': text,
            'sentences': [],
        }
        for sentence in doc.sents:
            current_sentence = {}
            current_sentence['sentence'] = sentence.text
            words = self.get_words(sentence.text)
            ners = self.get_ners(sentence.text)
            current_sentence['words'] = words
            current_sentence['ners'] = ners
            result['sentences'].append(current_sentence)
        logger.info('Text was processed')
        return result

    def get_words(self, sentence: str) -> list[dict]:
        doc = Doc(sentence)
        doc.segment(self.segmenter)
        doc.parse_syntax(self.syntax_parser)
        doc.tag_morph(self.morph_tagger)
        
        result = []
        
        for token in doc.tokens:
            if hasattr(token, 'rel'):
                head_word = next(
                    (t.text for t in doc.tokens if t.id == token.head_id),
                    ''
                )
                
                result.append(
                    {
                        'word': token.text,
                        'pos': token.pos,
                        'head_word': head_word,
                        'relation': token.rel,
                        'feats': str(token.feats)
                    }
                )
        return result
    
    def get_ners(self, sentence: str) -> list[dict]:
        doc = Doc(sentence)
        doc.segment(self.segmenter)
        doc.parse_syntax(self.syntax_parser)
        doc.tag_morph(self.morph_tagger)
        doc.tag_ner(self.ner_tagger)

        result = []

        for span in doc.spans:
            result.append({
                'ner': span.text,
                'type': span.type,
            })

        return result