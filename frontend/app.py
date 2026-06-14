from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

import math
import json
import sqlite3
import os
from pathlib import Path
from search.search import search
from search.autocomplete import get_suggestions
from rag.vector_search import search_chunks
from rag.rag_answer import answer_question
from flask import redirect


from rag.build_knowledge_base import (
    build_knowledge_base
)

from flask import redirect


from database.analytics import (
    create_tables,
    log_search,
    top_searches
)

app = Flask(__name__)
create_tables()

BASE_DIR = Path(__file__).resolve().parent.parent

DB_PATH = (
    BASE_DIR /
    "database" /
    "search.db"
)

INDEX_PATH = (
    BASE_DIR /
    "data" /
    "index.json"
)


# --------------------------------
# Home Page
# --------------------------------



@app.route(
    "/build",
    methods=["POST"]
)
def build():

    url = request.form.get(
        "url",
        ""
    ).strip()

    if not url:

        return redirect("/")

    try:

        build_knowledge_base(
            url
        )

    except Exception as e:

        print(
            "Build Error:",
            e
        )

    return redirect("/")











@app.route("/")
def home():

    query = request.args.get(
        "q",
        ""
    ).strip()

    page = int(
        request.args.get(
            "page",
            1
        )
    )

    results = []
    ai_answer = None
    total_results = 0
    total_pages = 0

    if query:
        try:
            log_search(query)
        except Exception as e: 
            print("LOG SEARCH ERROR:", e)

        try:
            data = search(
                query,
                page
                )
        except Exception as e:
                print("SEARCH ERROR:", repr(e))
                raise

        results = data["results"]

        total_results = data["total"]

        total_pages = math.ceil(
            total_results / 10
        )
        QUESTION_WORDS = [
        "what",
        "how",
        "why",
        "when",
        "where",
        "who",
        "which"
    ]
        is_question = any(
        query.lower().startswith(word)
        for word in QUESTION_WORDS
    )
        
        if is_question:

            try:

                ai_answer = answer_question(
                    query
            )

            except Exception as e:

                print(
                    "AI Error:",
                    e
            )

        print("TOTAL RESULTS =", total_results)
        print("PAGE =", page)
        print("RESULTS LENGTH =", len(results))

        if results:
            print("FIRST RESULT =", results[0])


    return render_template(
        "index.html",
        query=query,
        results=results,
        page=page,
        total_pages=total_pages,
        total_results=total_results,
        ai_answer=ai_answer
    )


# --------------------------------
# Autocomplete API
# --------------------------------

@app.route("/autocomplete")
def autocomplete():

    query = request.args.get(
        "q",
        ""
    )

    suggestions = get_suggestions(
        query
    )

    return jsonify(
        suggestions
    )


# --------------------------------
# Admin Dashboard
# --------------------------------

@app.route("/admin")
def admin():

    conn = sqlite3.connect(
        DB_PATH
    )

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM pages
        """
    )

    pages_count = cursor.fetchone()[0]

    conn.close()

    with open(
        INDEX_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        index = json.load(f)

    unique_words = len(index)

    db_size = round(
        os.path.getsize(DB_PATH)
        / 1024,
        2
    )

    popular_searches = (
        top_searches()
    )

    return render_template(
        "admin.html",
        pages=pages_count,
        unique_words=unique_words,
        db_size=db_size,
        popular=popular_searches
    )


# --------------------------------
# Run
# --------------------------------
@app.route("/ask")
def ask():

    question = request.args.get(
        "q",
        ""
    )

    answer = None

    if question:

        answer = answer_question(
            question
        )

    return render_template(
        "ask.html",
        question=question,
        answer=answer
    )


@app.route("/ai")
def ai_search():

    query = request.args.get(
        "q",
        ""
    )

    results = []

    if query:

        results = search_chunks(
            query,
            top_k=5
        )

    return render_template(
        "ai.html",
        query=query,
        results=results
    )

@app.route("/ask-ai")
def ask_ai():

    query = request.args.get(
        "q",
        ""
    )

    answer = None

    if query:

        answer = answer_question(
            query
        )

    return render_template(
        "ask_ai.html",
        query=query,
        answer=answer
    )









if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        ),
        debug=False
    )