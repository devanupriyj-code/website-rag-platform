import sqlite3
from pathlib import Path

DB_PATH = (
    Path(__file__).resolve().parent
    / "search.db"
)

def save_link(source, target):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO links
        (source,target)
        VALUES(?,?)
        """,
        (source,target)
    )

    conn.commit()
    conn.close()