import json
import spacy
from collections import Counter, defaultdict
from nltk.util import ngrams
from datetime import datetime
import re

# Загрузка данных
with open("chats/source_me_sample.json", "r", encoding="utf-8") as file:
    data = [json.loads(line) for line in file]

# Извлечение текстовых сообщений
texts = [entry["text"] for entry in data if isinstance(entry.get("text"), str) and entry["text"].strip()]

# Загрузка модели SpaCy
nlp = spacy.load("ru_core_news_sm")

# Анализ текста
all_tokens = []
custom_phrases = Counter()

for text in texts:
    # Токенизация текста
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct and token.is_alpha]
    all_tokens.extend(tokens)

    # Устойчивые фразы (биграммы и триграммы)
    for n in range(2, 4):
        ngram_phrases = ngrams(tokens, n)
        custom_phrases.update(ngram_phrases)

# Фильтрация фраз по частоте
filtered_phrases = [(phrase, count) for phrase, count in custom_phrases.items() if count > 5]
filtered_phrases = sorted(filtered_phrases, key=lambda x: x[1], reverse=True)

# Преобразование фраз в читаемый формат
readable_phrases = [" ".join(phrase) for phrase, _ in filtered_phrases]

# Сохранение результатов
results = {
    "most_common_phrases": readable_phrases
}

with open("chats/filtered_phrases_results.json", "w", encoding="utf-8") as result_file:
    json.dump(results, result_file, ensure_ascii=False, indent=4)

print("Анализ устойчивых фраз завершён. Результаты сохранены в 'chats/filtered_phrases_results.json'.")
