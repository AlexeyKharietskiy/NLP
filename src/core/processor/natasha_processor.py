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
            "texts": {
                "content": text
            },
            "sentences": [],
        }

        for sent_idx, sentence in enumerate(doc.sents, 1):
            sentence_text = sentence.text
            result["sentences"].append({
                "sentence": sentence_text,
                "order": sent_idx
            })
        

    def analyze_text(self, text, title="Untitled"):
        """
        Анализирует текст с помощью Natasha и возвращает структурированные данные.
        :param text: Входной текст
        :param title: Заголовок текста
        :return: Словарь с данными для таблиц texts, sentences, words, dependencies
        """
        # Анализируем текст с помощью Natasha
        doc = Doc(text)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        doc.parse_syntax(self.syntax_parser)

        # Формируем структуру данных
        result = {
            "texts": {
                "title": title,
                "content": text
            },
            "sentences": [],
            "words": [],
            "dependencies": []
        }

        # Временное сопоставление ID токенов Natasha с порядковыми номерами
        global_token_counter = 0  # Глобальный счётчик для токенов
        token_id_map = {}  # Для сопоставления Natasha ID с нашими ID

        # Обрабатываем предложения
        for sent_idx, sentence in enumerate(doc.sents, 1):
            # Текст предложения
            sentence_text = sentence.text
            # Добавляем предложение в результат
            result["sentences"].append({
                "sentence": sentence_text,
                "order": sent_idx
            })

            # Обрабатываем токены в предложении
            sentence_token_ids = []  # Для связи токенов с предложением
            for pos, token in enumerate(sentence.tokens):
                global_token_counter += 1
                token_id_map[token.id] = global_token_counter
                sentence_token_ids.append(global_token_counter)

                # Добавляем токен в результат
                result["words"].append({
                    "word": token.text,
                    "position": pos,
                    "sentence_id": sent_idx  # Для связи с предложением
                })

            # Обрабатываем зависимости
            for token in sentence.tokens:
                word_id = token_id_map[token.id]
                # Если head_id указывает на корень (root), ставим None
                head_id = token_id_map.get(token.head_id) if token.head_id and token.head_id != token.id else None
                result["dependencies"].append({
                    "word_id": word_id,
                    "head_id": head_id,
                    "relation": token.rel
                })

        return result
    
    