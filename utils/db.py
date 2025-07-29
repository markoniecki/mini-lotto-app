import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

DB_PATH = 'instance/mini_lotto.db'  # Jeden spójny plik bazy danych

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # Tabela użytkowników (bez emaila i is_active)
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Tabela propozycji artystycznych
    c.execute('''
        CREATE TABLE IF NOT EXISTS art_proposals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            text TEXT NOT NULL,
            created TEXT NOT NULL
        )
    ''')

    # Tabela postów forum
    c.execute('''
        CREATE TABLE IF NOT EXISTS forum_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            created TEXT NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def create_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        hashed = generate_password_hash(password)
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def validate_login(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    return row and check_password_hash(row[0], password)

def add_art_proposal(user, text):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO art_proposals (user, text, created) VALUES (?, ?, ?)",
              (user, text, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_all_proposals():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user, text, created FROM art_proposals ORDER BY created DESC")
    results = c.fetchall()
    conn.close()
    return results

def add_forum_post(user, title, content):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO forum_posts (user, title, content, created) VALUES (?, ?, ?, ?)",
              (user, title, content, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def get_all_forum_posts():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT user, title, content, created FROM forum_posts ORDER BY created DESC")
    results = c.fetchall()
    conn.close()
    return results
