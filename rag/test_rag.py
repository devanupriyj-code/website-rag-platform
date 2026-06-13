from rag.vector_search import (
    search_chunks
)

query = input(
    "Question: "
)

results = search_chunks(
    query
)

for i, (score, chunk) in enumerate(results, 1):

    print()
    print("=" * 50)

    print(
        f"Result {i}"
    )

    print(
        "Score:",
        round(score, 3)
    )

    print()

    print(
        chunk[:500]
    )