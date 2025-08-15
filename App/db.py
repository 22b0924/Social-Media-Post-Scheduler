import sqlite3
from contextlib import contextmanager
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "scheduler.db")

def init_db():
    with sqlite3.connect(DB_PATH) as c:
        c.execute("""CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            content TEXT,
            post_at TEXT,
            created_at TEXT,
            status TEXT,
            result TEXT
        )""")
        c.commit()

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    try:
        yield conn
    finally:
        conn.close()
