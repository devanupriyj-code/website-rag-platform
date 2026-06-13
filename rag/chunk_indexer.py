import sqlite3

from rag.chunker import (
    split_into_chunks
)

DB_PATH = "database/search.db"


def build_chunks():

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        content
    FROM pages
    """)

    pages = cursor.fetchall()

    cursor.execute(
        "DELETE FROM chunks"
    )

    for page_id, content in pages:

        chunks = split_into_chunks(
            content
        )

        for chunk in chunks:

            cursor.execute(
                """
                INSERT INTO chunks
                (
                    page_id,
                    content
                )
                VALUES (?, ?)
                """,
                (
                    page_id,
                    chunk
                )
            )

    conn.commit()

    conn.close()

    print(
        "Chunking Complete"
    )


if __name__ == "__main__":

    build_chunks()  