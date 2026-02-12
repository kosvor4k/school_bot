import requests
import time
import json
import os  # ← добавили для getenv

# Получаем токен из переменной окружения Bothost (не хардкодим!)
TOKEN = os.getenv('MAX_BOT_TOKEN')  # или 'MAX_BOT_TOKEN', 'BOT_TOKEN' — любой из списка выше

if not TOKEN:
    print("❌ Токен не найден в переменных окружения! Проверьте настройки бота на Bothost.")
    exit(1)  # Останавливаем бот, если токена нет

API_URL = "https://platform-api.max.ru"

HEADERS = {
    "Authorization": TOKEN,  # ← чистый токен (без Bearer, как работало в тестах)
    "Content-Type": "application/json"
}

# === ТЕКСТЫ === (без изменений, пропускаю для краткости)
WELCOME_TEXT = (
    "Здравствуйте! 👋\n"
    "Я — официальный бот **МКОУ «СОШ №15» ИМОСК** (станица Староизобильная).\n\n"
    # ... весь остальной текст ...
)

# ... (ADDRESS_TEXT, CONTACTS_TEXT и т.д. — оставь как было)

def get_inline_keyboard():
    # ... без изменений
    pass

def send_message(chat_id, text, keyboard=None, format_type="markdown"):
    # ... без изменений, но логирование оставь
    pass

def get_updates(marker=None):
    url = f"{API_URL}/updates"
    params = {"marker": marker, "timeout": 30} if marker is not None else {"timeout": 30}

    try:
        print(f"→ Запрос обновлений (marker={marker})")
        resp = requests.get(url, headers=HEADERS, params=params, timeout=40)
        
        print(f"← Статус: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"Ответ: {json.dumps(data, indent=2, ensure_ascii=False)}")
            return data
        else:
            print(f"Ошибка: {resp.status_code} — {resp.text}")
            return {}
    except Exception as e:
        print(f"Исключение: {e}")
        return {}

def handle_update(update):
    # ... без изменений (обработка сообщений, bot_started)
    pass

def main():
    print("✅ Бот запущен. Токен загружен из окружения:", "да" if TOKEN else "НЕТ")
    
    # Тест токена
    try:
        test_resp = requests.get(f"{API_URL}/me", headers=HEADERS, timeout=10)
        print(f"Тест /me → статус: {test_resp.status_code}")
        print(f"Ответ /me: {test_resp.text}")
    except Exception as e:
        print(f"Ошибка теста /me: {e}")

    marker = None
    
    while True:
        try:
            data = get_updates(marker)
            if not data:
                time.sleep(2)
                continue

            updates = data.get("updates", [])
            new_marker = data.get("marker")

            if updates:
                print(f"Получено обновлений: {len(updates)}")
                for update in updates:
                    handle_update(update)

            if new_marker is not None:
                marker = new_marker

            time.sleep(1.5)
            
        except Exception as e:
            print(f"Ошибка в цикле: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()