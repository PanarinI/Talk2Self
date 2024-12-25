import json
import spacy
from collections import Counter, defaultdict
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.util import ngrams
from datetime import datetime
import re

# Загрузка необходимых данных NLTK
nltk.download('punkt')
nltk.download('vader_lexicon')

# Загрузка данных
with open("chats/source_me_sample.json", "r", encoding="utf-8") as file:
    data = [json.loads(line) for line in file]

# Извлечение текстовых сообщений
texts = [entry["text"] for entry in data if isinstance(entry.get("text"), str) and entry["text"].strip()]
dates = [entry["date"] for entry in data if "date" in entry]

# Загрузка модели SpaCy
nlp = spacy.load("ru_core_news_sm")
sia = SentimentIntensityAnalyzer()

# Анализ структуры текста
question_count = 0
exclamation_count = 0
dots_count = 0
sentence_lengths = []
all_tokens = []
all_emojis = Counter()
custom_phrases = Counter()

emoji_pattern = re.compile(
    "[\U0001F600-\U0001F64F]|[\U0001F300-\U0001F5FF]|[\U0001F680-\U0001F6FF]|"
    "[\U0001F1E0-\U0001F1FF]|[\U00002500-\U00002BEF]|[\U00002702-\U000027B0]|"
    "[\U000024C2-\U0001F251]|[\U0001F926-\U0001FA9F]|[\U0001F900-\U0001F9FF]"
)

for text in texts:
    # Структурные анализы
    question_count += text.count("?")
    exclamation_count += text.count("!")
    dots_count += text.count("...")

    # Токенизация и эмодзи
    doc = nlp(text)
    tokens = [token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct]
    all_tokens.extend(tokens)

    # Эмодзи
    emojis = emoji_pattern.findall(text)
    all_emojis.update(emojis)

    # Средняя длина предложений
    sentences = [sent.text for sent in doc.sents]
    sentence_lengths.extend(len(sent.split()) for sent in sentences)

    # Устойчивые фразы
    for n in range(2, 4):
        ngram_phrases = ngrams(tokens, n)
        custom_phrases.update(ngram_phrases)


# Поведение по времени
hourly_activity = defaultdict(int)
for date in dates:
    hour = datetime.fromisoformat(date).hour
    hourly_activity[hour] += 1

# Частотный анализ
word_freq = Counter(all_tokens)
most_common_words = word_freq.most_common(20)
most_common_emojis = all_emojis.most_common(10)
most_common_phrases = custom_phrases.most_common(10)

# Результаты
results = {
    "question_count": question_count,
    "exclamation_count": exclamation_count,
    "dots_count": dots_count,
    "average_sentence_length": sum(sentence_lengths) / len(sentence_lengths),
    "hourly_activity": dict(hourly_activity),
    "most_common_words": most_common_words,
    "most_common_emojis": most_common_emojis,
    "most_common_phrases": [" ".join(phrase) for phrase, _ in most_common_phrases]
}

# Сохранение результатов
with open("chats/deep_analysis_results.json", "w", encoding="utf-8") as result_file:
    json.dump(results, result_file, ensure_ascii=False, indent=4)

print("Анализ завершён. Результаты сохранены в 'chats/deep_analysis_results.json'.")
