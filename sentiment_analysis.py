import json
from transformers import pipeline

# Загрузка модели для анализа тональности
sentiment_analyzer = pipeline("sentiment-analysis", model="blanchefort/rubert-base-cased-sentiment")

# Загрузка данных
with open("chats/source_me_sample.json", "r", encoding="utf-8") as file:
    data = [json.loads(line) for line in file]

# Извлечение текстовых сообщений
texts = [entry["text"] for entry in data if isinstance(entry.get("text"), str) and entry["text"].strip()]

# Анализ тональности
sentiment_results = {
    "positive": 0,
    "neutral": 0,
    "negative": 0,
    "details": []
}

for text in texts:
    result = sentiment_analyzer(text)[0]  # Анализируем текст
    label = result["label"].lower()  # Метка тональности (positive, neutral, negative)
    sentiment_results[label] += 1
    sentiment_results["details"].append({"text": text, "label": label, "score": result["score"]})

# Сохранение результатов
with open("chats/russian_sentiment_results.json", "w", encoding="utf-8") as result_file:
    json.dump(sentiment_results, result_file, ensure_ascii=False, indent=4)

print("Анализ тональности завершён. Результаты сохранены в 'chats/russian_sentiment_results.json'.")
