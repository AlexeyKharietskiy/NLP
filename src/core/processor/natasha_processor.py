import enum
from natasha import Segmenter, MorphVocab, NewsEmbedding, NewsSyntaxParser, Doc, NewsMorphTagger

from schemas.word_schemas import WordSchema

ud_relations_ru = {
    # Основные синтаксические роли
    'nsubj': 'подлежащее',
    'obj': 'прямое дополнение',
    'iobj': 'косвенное дополнение',
    'obl': 'обстоятельство',
    'vocative': 'обращение',
    'root': 'сказуемое',

    # Определения
    'amod': 'прилагательное-определение',
    'nmod': 'несогласованное определение',
    'appos': 'пояснение (приложение)',
    'nummod': 'числительное',
    'nummod:gov': 'числительное',
    
    # Глагольные конструкции
    'aux': 'вспомогательный глагол',
    'cop': 'связка (глагол-связка)',
    'xcomp': 'предикативное дополнение',
    'ccomp': 'дополнительное предложение',
    'advcl': 'обстоятельственное предложение',
    'csubj': 'придаточное-подлежащее',

    # Сочинительные связи
    'conj': 'однородный член',
    'cc': 'сочинительный союз',

    # Специальные конструкции
    'acl': 'определительное предложение',
    'acl:relcl': 'относительное предложение',
    'parataxis': 'вводная конструкция',
    'fixed': 'устойчивое выражение',
    'flat': 'составное слово',
    'flat:name': 'составное имя',

    # Служебные слова
    'case': 'предлог/послелог',
    'mark': 'подчинительный союз',
    'det': 'определитель (артикль/местоимение)',
    'advmod': 'наречие',
    'punct': 'знак препинания',
}
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
            if hasattr(token, 'rel') and token.rel not in (
                'punct', 
            ):
                head_word = next(
                    (t.text for t in doc.tokens if t.id == token.head_id),
                    ''
                )
                
                result.append(
                    WordSchema(
                        word=token.text,
                        head_word=head_word,
                        relation=ud_relations_ru.get(token.rel, ' ')
                    )
                )
        return result
    
processor = TextProcessor()