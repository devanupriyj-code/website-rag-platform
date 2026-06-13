import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "search.db"

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS pages(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT UNIQUE,
    title TEXT,
    content TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS searches(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT,
    searched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS links(
    source TEXT,
    target TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS chunks(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    page_id INTEGER,
    content TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS embeddings(
    chunk_id INTEGER,
    embedding TEXT
)
""")

conn.commit()
conn.close()

print("Database initialized.")