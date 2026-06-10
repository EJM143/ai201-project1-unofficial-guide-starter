from groq import Groq
import os
from dotenv import load_dotenv
from retrieval import search

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def ask(question):
    results = search(question, k=5)

    docs = results["documents"][0]
    metas = results["metadatas"][0]

    context = ""

    for doc, meta in zip(docs, metas):
        context += f"Professor: {meta['professor']}\n"
        context += f"Review: {doc}\n\n"

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "Answer ONLY using the provided context. "
                    "If context is insufficient, say: 'I don't have enough information.'"
                )
            },
            {
                "role": "user",
                "content": f"Context:\n{context}\n\nQuestion: {question}"
            }
        ]
    )

    return response.choices[0].message.content