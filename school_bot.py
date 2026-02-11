import requests
import time
import json

# === ТОКЕН БОТА ===
TOKEN = "f9LHodD0cOLFBjkYZrsosdv49516uFOuBXRhpjN8OYP4rf1MNiCFgUuNKxYSyUj0yIp5Yq36DwPvFF29T5hm"

API_URL = "https://platform-api.max.ru"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

# === ТЕКСТЫ ===
WELCOME_TEXT = (
    "Здравствуйте! 👋\n"
    "Я — официальный бот **МКОУ «СОШ №15» ИМОСК** (станица Староизобильная).\n\n"
    "Я могу рассказать вам:\n"
    "• 📍 **Адрес** школы\n"
    "• 📞 **Контактные телефоны и email**\n"
    "• 🕒 **Режим работы администрации**\n"
    "• 📝 **Как записать ребёнка в школу**\n"
    "• 🔗 **Полезные ссылки** (электронный дневник, сайт и др.)\n\n"
    "Просто выберите интересующий вас пункт ниже 👇"
)

ADDRESS_TEXT = (
    "📍 **Адрес школы**:\n"
    "356120, Ставропольский край, Изобильненский муниципальный округ,\n"
    "станица Староизобильная, улица Мира, дом 69."
)

CONTACTS_TEXT = (
    "📞 **Телефон**: 8 (86545) 4-51-17\n"
    "✉️ **Электронная почта**: starik.scool15@yandex.ru\n"
    "👩‍🏫 **Директор**: Наталья Андреевна Парохнина"
)

RECEPTION_TEXT = (
    "🕒 **Часы приёма директора**:\n"
    "Понедельник–пятница, с 8:00 до 16:00.\n\n"
    "Рекомендуем заранее позвонить для записи."
)

ENROLLMENT_TEXT = (
    "📝 **Зачисление в школу**:\n"
    "За МКОУ «СОШ №15» закреплены территории:\n"
    "• станица Староизобильная\n"
    "• хутор Смыков\n"
    "• хутор Сухой\n\n"
    "Подать заявление можно через портал **Госуслуги** → услуга «Запись в школу».\n\n"
    "❓Остались вопросы? Позвоните: 8 (86545) 4-51-17."
)

UNKNOWN_TEXT = (
    "❌ Я — **информационный бот МКОУ «СОШ №15»**.\n"
    "Могу помочь только по вопросам, связанным с **работой школы**.\n\n"
    "Пожалуйста, воспользуйтесь кнопками ниже или введите:\n"
    "`/start` — чтобы вернуть меню."
)

def get_inline_keyboard():
    return {
        "type": "inline_keyboard",
        "payload": {
            "buttons": [
                [
                    {"type": "message", "text": "📍 Адрес", "payload": "/address"},
                    {"type": "message", "text": "📞 Контакты", "payload": "/contacts"}
                ],
                [
                    {"type": "message", "text": "🕒 Приём", "payload": "/reception"},
                    {"type": "message", "text": "📝 Зачисление", "payload": "/enrollment"}
                ],
                [
                    {"type": "link", "text": "🌐 Сайт школы", "url": "https://school15-starizob.ru/"},
                    {"type": "link", "text": "📓 Эл. дневник", "url": "https://sgo.rkobr.ru/"}
                ]
            ]
        }
    }

def send_message(chat_id, text, keyboard=None, format_type="markdown"):
    url = f"{API_URL}/messages"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "format": format_type
    }
    if keyboard:
        payload["attachments"] = [keyboard]

    try:
        resp = requests.post(url, headers=HEADERS, json=payload, timeout=10)
        if resp.status_code != 200:
            print(f"Ошибка отправки сообщения: {resp.status_code} - {resp.text}")
        else:
            print(f"Сообщение отправлено в чат {chat_id}")
    except Exception as e:
        print(f"Исключение при отправке сообщения: {e}")

def get_updates(marker=None):
    url = f"{API_URL}/updates"
    params = {"marker": marker} if marker is not None else {}
    params["timeout"] = 30  # ← явно укажи таймаут, сервер может держать соединение дольше

    try:
        print(f"→ Запрос обновлений с marker={marker}")
        resp = requests.get(url, headers=HEADERS, params=params, timeout=40)
        
        print(f"← Статус: {resp.status_code}")
        if resp.status_code == 200:
            data = resp.json()
            print(f"Ответ сервера: {json.dumps(data, indent=2, ensure_ascii=False)}")  # ← полный дамп
            return data
        else:
            print(f"Ошибка: {resp.status_code} — {resp.text}")
            return {}
    except Exception as e:
        print(f"Исключение: {e}")
        return {}

def handle_update(update):
    if "message" in update and "text" in update["message"]:
        message = update["message"]
        chat_id = message["chat"]["id"]
        text = message.get("text", "").strip().lower()

        if text in ["/start", "/help"]:
            send_message(chat_id, WELCOME_TEXT, get_inline_keyboard())
        
        elif text == "/address":
            send_message(chat_id, ADDRESS_TEXT)
        
        elif text == "/contacts":
            send_message(chat_id, CONTACTS_TEXT)
        
        elif text == "/reception":
            send_message(chat_id, RECEPTION_TEXT)
        
        elif text == "/enrollment":
            send_message(chat_id, ENROLLMENT_TEXT)
        
        else:
            send_message(chat_id, UNKNOWN_TEXT, get_inline_keyboard())

    # Поддержка запуска через deep link (опционально)
    elif update.get("update_type") == "bot_started":
        chat_id = update.get("chat_id")
        payload = update.get("payload")
        print(f"Бот запущен через deep link, payload: {payload}")
        if chat_id:
            send_message(chat_id, WELCOME_TEXT, get_inline_keyboard())

def main():
    print("✅ Бот запущен. Ожидание сообщений...")
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
                print(f"Получено {len(updates)} обновлений")
                for update in updates:
                    handle_update(update)

            if new_marker is not None:
                marker = new_marker

            time.sleep(1.5)  # пауза, чтобы не превышать лимит 30 rps

        except Exception as e:
            print(f"Ошибка в главном цикле: {e}")
            time.sleep(5)  # пауза при серьёзной ошибке

if __name__ == "__main__":
    main()