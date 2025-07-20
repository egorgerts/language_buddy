import unittest
from app.utils import parse_text, save_to_db, init_db
import sqlite3
import os

class TestUtils(unittest.TestCase):
    def setUp(self):
        # Создаём тестовую БД
        self.test_db = 'db/test_language_buddy.db'
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        # Переопределяем путь к БД
        import app.utils
        app.utils.DB_PATH = self.test_db
        init_db()

    def tearDown(self):
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def test_parse_text(self):
        text = 'Hello world! This is a test.'
        words, phrases = parse_text(text)
        self.assertIn('Hello', words)
        self.assertIn('world', words)
        self.assertTrue(isinstance(words, list))
        self.assertTrue(isinstance(phrases, list))

    def test_save_to_db(self):
        words = ['cat', 'dog']
        phrases = ['black cat', 'big dog']
        save_to_db(words, phrases)
        conn = sqlite3.connect(self.test_db)
        c = conn.cursor()
        c.execute('SELECT word FROM words')
        db_words = [row[0] for row in c.fetchall()]
        c.execute('SELECT phrase FROM phrases')
        db_phrases = [row[0] for row in c.fetchall()]
        conn.close()
        self.assertIn('cat', db_words)
        self.assertIn('dog', db_words)
        self.assertIn('black cat', db_phrases)
        self.assertIn('big dog', db_phrases)

if __name__ == '__main__':
    unittest.main()
