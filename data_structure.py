import json
import pandas as pd

# Загружаем JSON
with open("chats/source_me.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Извлекаем список сообщений
messages = data.get("messages", [])
print(f"Всего сообщений: {len(messages)}")

# Фильтруем сообщения с текстом
filtered_messages = [msg for msg in messages if "text" in msg and msg["text"]]
print(f"Количество сообщений с текстом: {len(filtered_messages)}")
print(f"Пример сообщения: {filtered_messages[0]['text']}")

# Фильтруем по отправителю
filtered_by_sender = [msg for msg in filtered_messages if msg.get("from") == "Игорь"]
print(f"Количество сообщений от Игоря: {len(filtered_by_sender)}")
print(f"Пример сообщения от Игоря: {filtered_by_sender[0]['text']}")

# Преобразуем в DataFrame
df = pd.DataFrame(filtered_by_sender)

# Проверяем данные
print(df.head())

# Убираем лишние столбцы, оставляем только текст и дату
df_cleaned = df[["text"]]
print(df_cleaned.head())

print("Количество сообщений:", len(messages))


# Сохраняем выборку в файл
sample_df = df_cleaned.sample(n=min(len(df_cleaned), 10000), random_state=42)  # Выборка до 10,000 сообщений
sample_df.to_json("chats/source_me_sample.json", orient="records", lines=True, force_ascii=False)

print("Выборка сохранена в файл 'chats/source_me_sample.json'")
