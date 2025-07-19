import sqlite3

def get_words_and_phrases():
    conn = sqlite3.connect('db/language_buddy.db')
    c = conn.cursor()
    c.execute('SELECT word, translation FROM words')
    words = c.fetchall()
    c.execute('SELECT phrase, translation FROM phrases')
    phrases = c.fetchall()
    conn.close()
    return words, phrases

# TODO: добавить функции для перевода и генерации карточек
