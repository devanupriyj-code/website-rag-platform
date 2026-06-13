import json
import sqlite3
from pathlib import Path

# -----------------------------
# Paths
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

INDEX_PATH = BASE_DIR / "data" / "index.json"
IDF_PATH = BASE_DIR / "data" / "idf.json"
DB_PATH = BASE_DIR / "database" / "search.db"

# -----------------------------
# Load Index (reload when files change)
# -----------------------------

_index = None
_idf = None
_index_mtime = None


def load_search_data():

    global _index, _idf, _index_mtime

    mtime = INDEX_PATH.stat().st_mtime

    if _index is None or mtime != _index_mtime:

        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            _index = json.load(f)

        with open(IDF_PATH, "r", encoding="utf-8") as f:
            _idf = json.load(f)

        _index_mtime = mtime

    return _index, _idf

# -----------------------------
# Helpers
# -----------------------------

def get_snippet(text, query_words):

    text_lower = text.lower()

    for word in query_words:

        pos = text_lower.find(word.lower())

        if pos != -1:

            start = max(0, pos - 60)
            end = min(len(text), pos + 120)

            return text[start:end] + "..."

    return text[:180] + "..."


def highlight(text, query_words):

    result = text

    for word in query_words:

        result = result.replace(
            word,
            f"<mark>{word}</mark>"
        )

        result = result.replace(
            word.capitalize(),
            f"<mark>{word.capitalize()}</mark>"
        )

        result = result.replace(
            word.upper(),
            f"<mark>{word.upper()}</mark>"
        )

    return result


# -----------------------------
# Database
# -----------------------------

def get_pages(doc_ids):

    if not doc_ids:
        return {}

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    placeholders = ",".join(
        "?" * len(doc_ids)
    )

    cursor.execute(
        f"""
        SELECT
            id,
            title,
            url,
            content
        FROM pages
        WHERE id IN ({placeholders})
        """,
        tuple(doc_ids)
    )

    rows = cursor.fetchall()

    conn.close()

    pages = {}

    for row in rows:

        pages[row[0]] = {
            "title": row[1],
            "url": row[2],
            "content": row[3]
        }

    return pages


# -----------------------------
# Phrase Search
# -----------------------------

def phrase_search(
    phrase,
    page=1,
    per_page=10
):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        title,
        url,
        content
    FROM pages
    """)

    rows = cursor.fetchall()

    conn.close()

    phrase = phrase.lower()

    matches = []

    for row in rows:

        title = row[1]
        url = row[2]
        content = row[3]

        if phrase in content.lower():

            snippet = get_snippet(
                content,
                phrase.split()
            )

            snippet = highlight(
                snippet,
                phrase.split()
            )

            matches.append({
                "title": title,
                "url": url,
                "score": "Phrase Match",
                "snippet": snippet
            })

    total = len(matches)

    start = (page - 1) * per_page
    end = start + per_page

    return {
        "results": matches[start:end],
        "total": total
    }


# -----------------------------
# TF-IDF Search
# -----------------------------

def tfidf_search(
    query,
    page=1,
    per_page=10
):

    index, idf = load_search_data()

    query_words = query.lower().split()

    scores = {}

    for word in query_words:

        if word not in index:
            continue

        for doc_id, tf in index[word].items():

            doc_id = int(doc_id)

            score = tf * idf[word]

            scores[doc_id] = (
                scores.get(doc_id, 0)
                + score
            )

    ranked = sorted(
        scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    total = len(ranked)

    start = (page - 1) * per_page
    end = start + per_page

    page_ranked = ranked[start:end]

    top_doc_ids = [
        doc_id
        for doc_id, _
        in page_ranked
    ]

    pages = get_pages(
        top_doc_ids
    )

    if top_doc_ids and not pages:
        print(
            "SEARCH WARNING: index returned",
            len(top_doc_ids),
            "doc IDs but get_pages() found none.",
            "Sample index IDs:",
            top_doc_ids[:5],
            "- rebuild index after crawling."
        )

    results = []

    for doc_id, score in page_ranked:

        if doc_id not in pages:
            continue

        page_data = pages[doc_id]

        snippet = get_snippet(
            page_data["content"],
            query_words
        )

        snippet = highlight(
            snippet,
            query_words
        )

        results.append({
            "title": page_data["title"],
            "url": page_data["url"],
            "score": round(score, 2),
            "snippet": snippet
        })

    return {
        "results": results,
        "total": total
    }


# -----------------------------
# Main Search
# -----------------------------

def search(
    query,
    page=1,
    per_page=10
):

    query = query.strip()

    if (
        query.startswith('"')
        and
        query.endswith('"')
    ):

        phrase = query[1:-1]

        return phrase_search(
            phrase,
            page,
            per_page
        )

    return tfidf_search(
        query,
        page,
        per_page
    )


# -----------------------------
# Debug
# -----------------------------

if __name__ == "__main__":

    while True:

        query = input("\nSearch: ")

        data = search(query)

        print(
            "\nTotal Results:",
            data["total"]
        )

        for result in data["results"]:

            print("\n------------------")
            print(result["title"])
            print(result["url"])
            print("Score:", result["score"])