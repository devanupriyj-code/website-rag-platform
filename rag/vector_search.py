import json
import sqlite3
import numpy as np

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

DB_PATH = "database/search.db"


def cosine_similarity(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.dot(a, b) / (
        np.linalg.norm(a)
        *
        np.linalg.norm(b)
    )


def search_chunks(
    query,
    top_k=5
):

    query_embedding = model.encode(
        query
    )

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        embeddings.chunk_id,
        embeddings.embedding,
        chunks.content
    FROM embeddings
    JOIN chunks
    ON embeddings.chunk_id = chunks.id
    """)

    rows = cursor.fetchall()

    conn.close()

    scores = []

    for chunk_id, emb_json, content in rows:

        embedding = json.loads(
            emb_json
        )

        score = cosine_similarity(
            query_embedding,
            embedding
        )

        scores.append(
            (
                score,
                content
            )
        )

    scores.sort(
        reverse=True,
        key=lambda x: x[0]
    )

    return scores[:top_k]