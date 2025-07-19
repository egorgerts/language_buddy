
from flask import Flask, render_template, request, redirect
from app.utils import parse_text, save_to_db, init_db
from app.db_api import get_words_and_phrases
from app.translate_api import update_translations
import os

app = Flask(__name__, template_folder=os.path.join(os.path.dirname(__file__), '../templates'))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form.get('text')
        words, phrases = parse_text(text)
        save_to_db(words, phrases)
        # Переводим слова и выражения
        update_translations()
        db_words, db_phrases = get_words_and_phrases()
        return render_template('index.html', text=text, words=db_words, phrases=db_phrases)
    db_words, db_phrases = get_words_and_phrases()
    return render_template('index.html', words=db_words, phrases=db_phrases)

if __name__ == '__main__':
    # Инициализация базы данных при первом запуске
    if not os.path.exists('db/language_buddy.db'):
        init_db()
    app.run(debug=True)
