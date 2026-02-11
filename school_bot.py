import requests
import time
import json

# === НАСТРОЙКИ ===
TOKEN = "f9LHodD0cOLFBjkYZrsosdv49516uFOuBXRhpjN8OYP4rf1MNiCFgUuNKxYSyUj0yIp5Yq36DwPvFF29T5hm"  # ← Замените на реальный токен
API_URL = "https://platform-api.max.ru"
HEADERS = {
    "Authorization": TOKEN,
    "Content-Type": "application/json"
}

# === ТЕКСТЫ ОТВЕТОВ ===
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

# === INLINE-КЛАВИАТУРА ===
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

# === ОТПРАВКА СООБЩЕНИЯ ===
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
        response = requests.post(url, headers=HEADERS, json=payload)
        if response.status_code != 200:
            print(f"Ошибка отправки: {response.status_code} — {response.text}")
    except Exception as e:
        print(f"Исключение при отправке: {e}")

# === ПОЛУЧЕНИЕ ОБНОВЛЕНИЙ ===
def get_updates(offset=None):
    url = f"{API_URL}/updates"
    params = {"offset": offset} if offset else {}
    try:
        response = requests.get(url, headers=HEADERS, params=params, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Ошибка получения обновлений: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Исключение при получении обновлений: {e}")
        return {}

# === ОБРАБОТКА СООБЩЕНИЯ ===
def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "").strip()

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
        send_message(chat_id, UNKNOWN_TEXT)

# === ОСНОВНОЙ ЦИКЛ ===
def main():
    print("✅ Бот запущен. Ожидание сообщений...")
    offset = None
    while True:
        updates = get_updates(offset)
        for update in updates.get("updates", []):
            if "message" in update and "text" in update["message"]:
                handle_message(update["message"])
            offset = update["update_id"] + 1
        time.sleep(1)

if __name__ == "__main__":
    main()