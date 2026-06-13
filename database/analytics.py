import sqlite3
from pathlib import Path

DB_PATH = (
    Path(__file__).resolve().parent
    / "search.db"
)

def log_search(query):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO searches(query)
        VALUES(?)
        """,
        (query,)
    )

    conn.commit()
    conn.close()

def top_searches(limit=10):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            query,
            COUNT(*) as count
        FROM searches
        GROUP BY query
        ORDER BY count DESC
        LIMIT ?
        """,
        (limit,)
    )

    rows = cursor.fetchall()

    conn.close()

    return rows