
import openai
import os

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPENAI_API_KEY

def translate(text: str) -> str:
    prompt = f"Переведи на русский язык: {text}"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=60
    )
    return response.choices[0].message['content'].strip()

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
