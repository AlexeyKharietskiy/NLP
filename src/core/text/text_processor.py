import enum
from natasha import Doc, Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger

from schemas.words import WordSchema

class WordPos(enum.Enum):
    NOUN = "имя существительное"
    ADJ = "имя прилагательное"
    VERB = "глагол"
    INFN = "инфинитив"
    PRTF = "причастие"
    PRTS = "деепричастие"
    NUMR = "числительное"
    ADV = "наречие"
    PRON = "местоимение"
    PRED = "предикатив"
    ADP = "предлог"
    SCONJ = "подчинительный союз"
    CCONJ = "сочинительный союз"
    PART = "частица"
    INTJ = "междометие"
    PROPN = "название"
    DET = 'определитель'
class TextProcessor:
    def __init__(self):
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        self.morph_tagger = NewsMorphTagger(NewsEmbedding())
        self.doc = Doc
    
    def get_tokens(self, text: str) -> list[WordSchema]:
        '''Input data - text'''
        lower_text = text.lower()
        self.doc = Doc(lower_text)
        self.doc.segment(self.segmenter)
        self.doc.tag_morph(self.morph_tagger)
        tokens = []
        for token in self.doc.tokens:
            if token.pos in {
                "NOUN", "VERB", "ADJ", "NUMR"
                "ADV", "PRON", "PROPN", "PART", 
                "CCONJ", "SCONJ", "ADP", "DET",
                "INFN", 'PRTF', 'PRTS', 'PRED',
                'INTJ'
                }:
                token.lemmatize(self.morph_vocab)
                curr_token = WordSchema(
                    word=token.text, 
                    lemma= token.lemma, 
                    part_of_speech= WordPos[token.pos],
                    frequency= 1,
                    feats= str(token.feats)
                )
                if curr_token not in tokens:
                    tokens.append(curr_token)
                else: 
                    for i, tok in enumerate(tokens):
                        if tok == curr_token:
                            tokens[i].frequency+=1                            
        return tokens
    
    
processor = TextProcessor()