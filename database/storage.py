import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "search.db"


def save_page(page):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT OR IGNORE INTO pages
    (url, title, content)
    VALUES (?, ?, ?)
    """, (
        page["url"],
        page["title"],
        page["content"]
    ))

    conn.commit()
    conn.close()