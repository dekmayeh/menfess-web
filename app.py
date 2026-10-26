from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)

# Path database (penting untuk PythonAnywhere)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, 'menfess.db')

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS menfess (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                message TEXT NOT NULL,
                nickname TEXT DEFAULT 'Anonim',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()

@app.route('/')
def index():
    conn = get_db()
    menfess_list = conn.execute(
        'SELECT * FROM menfess ORDER BY created_at DESC'
    ).fetchall()
    conn.close()
    return render_template('index.html', menfess_list=menfess_list)

@app.route('/kirim', methods=['GET', 'POST'])
def kirim():
    if request.method == 'POST':
        message = request.form.get('message', '').strip()
        nickname = request.form.get('nickname', '').strip() or 'Anonim'

        if message:
            conn = get_db()
            conn.execute(
                'INSERT INTO menfess (message, nickname) VALUES (?, ?)',
                (message, nickname)
            )
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    
    return render_template('kirim.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
