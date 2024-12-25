import json

# Загружаем JSON
with open("chats/source_me.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Проверяем ключи словаря
print("Ключи:", data.keys())

# Предполагаем, что ключ 'messages' содержит нужные данные
if "messages" in data:
    messages = data["messages"]
    print("Количество сообщений:", len(messages))
    print("Пример сообщения:", messages[0])
else:
    print("Ключ 'messages' не найден. Проверьте структуру JSON.")
