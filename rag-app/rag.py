from dotenv import load_dotenv
from groq import Groq
from build_index import search

load_dotenv()
client = Groq(timeout=60.0, max_retries=5)


def answer(question):
    chunks = search(question, n=4)
    context = "\n\n".join(f"[Page {c['page']}]\n{c['text']}" for c in chunks)

    prompt = f"""Answer the question using ONLY the context below.
Cite page numbers like (p. 5). If the answer is not in the context,
say "I couldn't find that in the document."

Context:
{context}

Question: {question}"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        max_tokens=1500,
        messages=[{"role": "user", "content": prompt}],
    )
    pages = sorted({c["page"] for c in chunks})
    return response.choices[0].message.content, pages


if __name__ == "__main__":
    while True:
        q = input("\nAsk a question (or type quit): ")
        if q.lower() == "quit":
            break
        text, pages = answer(q)
        print("\n" + text)
        print("Sources: pages", pages)
