import pandas as pd
import json

# Загружаем JSON
with open("chat_logs.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Преобразуем в DataFrame
df = pd.DataFrame(data)

# Проверяем первые строки
print(df.head())
