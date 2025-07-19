import sqlite3
from typing import List, Tuple
import re

DB_PATH = 'db/language_buddy.db'

# Функция для разбора текста на слова и словосочетания

def parse_text(text: str) -> Tuple[List[str], List[str]]:
    # Простая токенизация: слова и словосочетания
    words = re.findall(r'\b\w+\b', text)
    phrases = re.findall(r'\b\w+(?:\s+\w+)+\b', text)
    return words, phrases

# Функция для инициализации базы данных

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT UNIQUE,
        translation TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS phrases (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        phrase TEXT UNIQUE,
        translation TEXT
    )''')
    conn.commit()
    conn.close()

# Функция для сохранения слов и словосочетаний

def save_to_db(words: List[str], phrases: List[str]):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    for word in words:
        c.execute('INSERT OR IGNORE INTO words (word) VALUES (?)', (word,))
    for phrase in phrases:
        c.execute('INSERT OR IGNORE INTO phrases (phrase) VALUES (?)', (phrase,))
    conn.commit()
    conn.close()

# TODO: добавить функции для перевода и генерации карточек
