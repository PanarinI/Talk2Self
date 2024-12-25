import json
import spacy
from collections import Counter
from itertools import islice
import nltk

# Загрузка необходимых данных NLTK
nltk.download('punkt')
nltk.download('stopwords')

# Загрузка данных
with open("chats/source_me_sample.json", "r", encoding="utf-8") as file:
    data = [json.loads(line) for line in file]

# Извлечение текстовых сообщений
texts = [entry["text"] for entry in data if isinstance(entry.get("text"), str) and entry["text"].strip()]

# Загрузка модели SpaCy
nlp = spacy.load("ru_core_news_sm")

# Токенизация и анализ
all_tokens = []
for text in texts:
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
    all_tokens.extend(tokens)

# Частотный анализ слов
word_freq = Counter(all_tokens)

# Топ-20 частых слов
most_common_words = word_freq.most_common(20)
print("Топ-20 слов:")
for word, freq in most_common_words:
    print(f"{word}: {freq}")

# Анализ биграмм
from nltk.util import ngrams
bigrams = list(ngrams(all_tokens, 2))
bigram_freq = Counter(bigrams)

# Топ-10 биграмм
most_common_bigrams = bigram_freq.most_common(10)
print("\nТоп-10 биграмм:")
for bigram, freq in most_common_bigrams:
    print(f"{' '.join(bigram)}: {freq}")

# Характеристики сообщений
avg_length = sum(len(text.split()) for text in texts) / len(texts)
print(f"\nСредняя длина сообщений: {avg_length:.2f} слов")

# Сохранение результатов
with open("chats/me_analysis_results.json", "w", encoding="utf-8") as result_file:
    json.dump({
        "most_common_words": most_common_words,
        "most_common_bigrams": most_common_bigrams,
        "average_message_length": avg_length
    }, result_file, ensure_ascii=False, indent=4)

print("\nАнализ завершён. Результаты сохранены в 'chats/me_analysis_results.json'.")
