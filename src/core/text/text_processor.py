from natasha import Doc, Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger

class TextProcessor:
    def __init__(self):
        self.segmenter = Segmenter()
        self.morph_vocab = MorphVocab()
        self.morph_tagger = NewsMorphTagger(NewsEmbedding())
        self.doc = Doc
        
    def process(self, text: str):
        ...
        
    def get_sentences(self, text: str):
        sentences = list(self.segmenter.analyze(text))
        return sentences
    
    def get_tokens(self, sentence: str):
        '''Input data sentence from TextProcessor.get_sentences'''
        lower_text = sentence.lower()
        self.doc = Doc(lower_text)
        self.doc.segment(self.segmenter)
        self.doc.tag_morph(self.morph_tagger)
        tokens = []
        for token in self.doc.tokens:
            if token.pos in {
                "NOUN", "VERB", "ADJ", "NUM"
                "ADV", "PRON", "PROPN", "PART", 
                "CCONJ", "SCONJ", "ADP", "DET" 
                }:
                token.lemmatize(self.morph_vocab)
                curr_token = {
                    'wordform':token.text,
                    'lemma':token.lemma,
                    'pos':token.pos,
                    'feats':token.feats
                    }
                tokens.append(curr_token)
        return tokens
    
    
processor = TextProcessor()