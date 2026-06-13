import sqlite3

from crawler.threaded_crawler_v2 import (
    crawl_site
)

from indexer.indexer import (
    build_index
)

from rag.chunk_indexer import (
    build_chunks
)

from rag.embed_chunks import (
    build_embeddings
)

DB_PATH = "database/search.db"


def clear_old_data():

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM pages"
    )

    cursor.execute(
        "DELETE FROM links"
    )

    cursor.execute(
        "DELETE FROM chunks"
    )

    cursor.execute(
        "DELETE FROM embeddings"
    )

    cursor.execute(
        """
        DELETE FROM sqlite_sequence
        WHERE name IN ('pages', 'chunks')
        """
    )

    conn.commit()

    conn.close()


def build_knowledge_base(
    url
):

    print()
    print(
        "===== BUILDING KNOWLEDGE BASE ====="
    )

    print()
    print(
        "Clearing old data..."
    )

    clear_old_data()

    print()
    print(
        "Crawling..."
    )

    crawl_site(
        url,
        max_pages=100
    )

    print()
    print(
        "Building search index..."
    )

    build_index()

    print()
    print(
        "Chunking..."
    )

    build_chunks()

    print()
    print(
        "Embedding..."
    )

    build_embeddings()

    print()
    print(
        "Knowledge Base Ready!"
    )