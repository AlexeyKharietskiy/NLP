from natasha import Segmenter, MorphVocab, NewsEmbedding, NewsSyntaxParser, Doc, NewsMorphTagger

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
        result = {
            "sentences": [],
        }

        for sent_idx, sentence in enumerate(doc.sents, 1):
            sentence_text = sentence.text
            result["sentences"].append({
                "sentence": sentence_text,
                "order": sent_idx
            })
        return result

    def get_words(self, sentence: str):
        doc = Doc(sentence)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_vocab)
        doc.parse_syntax(self.syntax_parser)
        sent = doc.sents[0]
        result =  {
            'words': []
        }
        for pos, token in enumerate(sent):
            if token.pos in {
                "NOUN", "VERB", "ADJ", "NUMR"
                "ADV", "PRON", "PROPN", "PART", 
                "CCONJ", "SCONJ", "ADP", "DET",
                "INFN", 'PRTF', 'PRTS', 'PRED',
                'INTJ'
                }:
                    result["words"].append({
                        "word": token.text,
                        "position": pos,
                        'head': [head.word for head in sentence.tokens if head.id == token.head_id][0],
                        'rel': token.rel
                    })
                
        return result