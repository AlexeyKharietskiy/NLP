def get_concordances(texts, target_word, context_size=5):
    concordances = []

    for text in texts:
        words = text.content.split()  # Разделяем текст на слова
        for i, word in enumerate(words):
            if word == target_word or word == target_word.capitalize():
                # Собираем контекст
                left_context = words[max(0, i - context_size):i]
                right_context = words[i + 1:i + 1 + context_size]
                concordances.append({
                    "word": word,
                    "left_context": left_context,
                    "right_context": right_context,
                    'text_title': text.title
                })

    return concordances