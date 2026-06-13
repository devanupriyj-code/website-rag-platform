import json
import sqlite3

from sentence_transformers import (
    SentenceTransformer
)

DB_PATH = "database/search.db"

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def build_embeddings():

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM embeddings"
    )

    cursor.execute("""
    SELECT
        id,
        content
    FROM chunks
    """)

    chunks = cursor.fetchall()

    total = len(chunks)

    for i, (chunk_id, content) in enumerate(
        chunks,
        start=1
    ):

        embedding = model.encode(
            content
        ).tolist()

        cursor.execute(
            """
            INSERT INTO embeddings
            (
                chunk_id,
                embedding
            )
            VALUES (?, ?)
            """,
            (
                chunk_id,
                json.dumps(
                    embedding
                )
            )
        )

        if i % 10 == 0:

            print(
                f"Embedded {i}/{total}"
            )

    conn.commit()

    conn.close()

    print(
        "Embeddings Created"
    )


if __name__ == "__main__":

    build_embeddings()