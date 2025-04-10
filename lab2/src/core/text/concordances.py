import  re

def get_concordances(texts, target_word: str, context_size=5):
    concordances = []

    pattern = re.compile(rf'\b{re.escape(target_word)}(?=\W|\b)', flags=re.IGNORECASE)

    for text in texts:
        tokens = re.findall(r'\S+\s*', text.content)
        for i, token in enumerate(tokens):
            clean_word = token.strip()
            if pattern.search(clean_word):
                left_context = tokens[max(0, i - context_size):i]
                right_context = tokens[i + 1:i + 1 + context_size]

                left_str = ''.join(left_context).strip()
                right_str = ''.join(right_context).strip()

                concordances.append({
                    "word": clean_word,
                    "left_context": left_context,
                    "right_context": right_context,
                    'text_title': text.title
                })
                
    return concordances