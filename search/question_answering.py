from search.search import search


def answer_question(question):

    data = search(question)

    results = data["results"]

    if not results:

        return {
            "answer": "No answer found.",
            "source": None
        }

    top_result = results[0]

    snippet = top_result["snippet"]

    return {
        "answer": snippet,
        "source": top_result["url"]
    }