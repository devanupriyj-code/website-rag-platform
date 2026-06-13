import os

from groq import Groq
from rag.vector_search import search_chunks

client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)

def answer_question(question):

    chunks = search_chunks(
        question,
        top_k=5
    )

    context = "\n\n".join(
        chunk
        for _, chunk in chunks
    )

    prompt = f"""
Answer using ONLY the provided context.

Context:
{context}

Question:
{question}

Give a concise answer.
"""

    response = (
        client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
    )

    answer = (
        response
        .choices[0]
        .message
        .content
    )

    return {
        "answer": answer,
        "chunks": chunks
    }