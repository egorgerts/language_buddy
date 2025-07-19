import requests
YANDEX_API_KEY = os.getenv('YANDEX_API_KEY')
YANDEX_FOLDER_ID = os.getenv('YANDEX_FOLDER_ID')

def yandex_translate(text: str) -> str:
    if not YANDEX_API_KEY:
        return "Перевод недоступен (нет ключа Яндекс)"
    url = "https://translate.api.cloud.yandex.net/translate/v2/translate"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Api-Key {YANDEX_API_KEY}"
    }
    data = {
        "folder_id": YANDEX_FOLDER_ID,
        "texts": [text],
        "targetLanguageCode": "ru"
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        return result["translations"][0]["text"]
    except Exception:
        return "Перевод недоступен (ошибка Яндекс)"


import openai
import os
from dotenv import load_dotenv

load_dotenv()
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def translate(text: str) -> str:
    prompt = f"Переведи на русский язык: {text}"
    client = openai.OpenAI(api_key=OPENAI_API_KEY)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=60
        )
        return response.choices[0].message.content.strip()
    except openai.RateLimitError:
        # Если квота OpenAI исчерпана, используем Яндекс
        return yandex_translate(text)

import sqlite3

def update_translations():
    conn = sqlite3.connect('db/language_buddy.db')
    c = conn.cursor()
    # Переводим слова
    c.execute('SELECT id, word FROM words WHERE translation IS NULL')
    for row in c.fetchall():
        word_id, word = row
        translation = translate(word)
        c.execute('UPDATE words SET translation=? WHERE id=?', (translation, word_id))
    # Переводим словосочетания
    c.execute('SELECT id, phrase FROM phrases WHERE translation IS NULL')
    for row in c.fetchall():
        phrase_id, phrase = row
        translation = translate(phrase)
        c.execute('UPDATE phrases SET translation=? WHERE id=?', (translation, phrase_id))
    conn.commit()
    conn.close()
