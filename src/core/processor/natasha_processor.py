import enum
from natasha import Segmenter, MorphVocab, NewsEmbedding, NewsSyntaxParser, Doc, NewsMorphTagger

from schemas.word_schemas import WordSchema

ud_relations_ru = {
    'acl': 'относительное предложение',
    'acl:relcl': 'относительное предложение (специфическое)',
    'advcl': 'обстоятельственное придаточное',
    'advmod': 'обстоятельство',
    'amod': 'согласованное определение',
    'appos': 'приложение',
    'aux': 'вспомогательный глагол',
    'aux:pass': 'вспомогательный глагол (пассив)',
    'case': 'предлог/послелог',
    'cc': 'сочинительный союз',
    'ccomp': 'дополнительное придаточное',
    'clf': 'классификатор',
    'compound': 'составная часть',
    'conj': 'сочинительная связь',
    'cop': 'связка',
    'csubj': 'предикативное придаточное',
    'csubj:pass': 'предикативное придаточное (пассив)',
    'dep': 'неопределенная зависимость',
    'det': 'определитель',
    'discourse': 'дискурсивный элемент',
    'dislocated': 'дислоцированный элемент',
    'expl': 'эксплетив (формальный субъект)',
    'fixed': 'фиксированное выражение',
    'flat': 'плоская структура',
    'flat:foreign': 'иностранное слово в составе',
    'flat:name': 'имя собственное (составное)',
    'goeswith': 'графическое объединение',
    'iobj': 'косвенное дополнение',
    'list': 'элемент списка',
    'mark': 'подчинительный союз',
    'nmod': 'несогласованное определение',
    'nsubj': 'подлежащее',
    'nsubj:outer': 'внешнее подлежащее',
    'nsubj:pass': 'подлежащее (пассив)',
    'nummod': 'числительное как модификатор',
    'nummod:entity': 'числительное-сущность',
    'nummod:gov': 'числительное-главное слово',
    'obj': 'прямое дополнение',
    'obl': 'косвенное дополнение',
    'obl:agent': 'агентивное дополнение',
    'obl:tmod': 'временное обстоятельство',
    'orphan': 'сиротский элемент (в эллипсисе)',
    'parataxis': 'паратаксис',
    'punct': 'знак препинания',
    'reparandum': 'элемент для исправления',
    'root': 'корневой элемент (сказуемое)',
    'vocative': 'вокатив',
    'xcomp': 'предикативное дополнение',
    
    # Специфические для русского языка
    'nmod:agent': 'агентивное определение',
    'nmod:gsubj': 'глагольное подлежащее',
    'nmod:gobj': 'глагольное дополнение',
    'nmod:poss': 'притяжательное определение',
}
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
                        relation=ud_relations_ru[token.rel]
                    )
                )
        
        return result