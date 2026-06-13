import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "search.db"

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM pages")

count = cursor.fetchone()[0]

print("Pages:", count)

conn.close()