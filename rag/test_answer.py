from rag.rag_answer import answer_question

while True:

    question = input(
        "Question: "
    )

    answer = answer_question(
        question
    )

    print()
    print(answer)
    print()