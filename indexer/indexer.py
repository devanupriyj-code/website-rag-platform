import sqlite3
import json
import math
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = BASE_DIR / "database" / "search.db"

INDEX_PATH = BASE_DIR / "data" / "index.json"
IDF_PATH = BASE_DIR / "data" / "idf.json"

# -----------------------------
# Stop Words
# -----------------------------

STOP_WORDS = {
    "the", "a", "an",
    "and", "or",
    "is", "are",
    "to", "of",
    "for", "in",
    "on", "with",
    "at", "by",
    "from", "as",
    "be", "was",
    "were", "it",
    "this", "that"
}


def build_index():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, content
    FROM pages
    """)

    rows = cursor.fetchall()

    conn.close()

    index = {}

    total_docs = len(rows)

    for row in rows:

        doc_id = row[0]
        content = row[1]

        words = content.lower().split()

        for word in words:

            word = word.strip(
                ".,!?;:\"'()[]{}<>|\\/`~@#$%^&*-_=+"
            )

            if not word:
                continue

            if word in STOP_WORDS:
                continue

            if word not in index:
                index[word] = {}

            index[word][str(doc_id)] = (
                index[word].get(str(doc_id), 0)
                + 1
            )

    idf = {}

    for word in index:

        docs_with_word = len(index[word])

        idf[word] = (
            math.log(
                (total_docs + 1)
                /
                (docs_with_word + 1)
            ) + 1
        )

    with open(
        INDEX_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            index,
            f,
            indent=4
        )

    with open(
        IDF_PATH,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            idf,
            f,
            indent=4
        )

    print()
    print("===== INDEXING COMPLETE =====")
    print("Documents Indexed :", total_docs)
    print("Unique Words      :", len(index))
    print()

    return {
        "total_docs": total_docs,
        "unique_words": len(index)
    }


if __name__ == "__main__":

    build_index()
