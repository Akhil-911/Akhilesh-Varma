import chromadb
from load_pdf import build_chunks

client = chromadb.PersistentClient(path="chroma_db")   # saves to disk
collection = client.get_or_create_collection(name="docs")

def build_index(pdf_path):
    """Chunk the PDF and store every chunk in the vector database."""
    chunks = build_chunks(pdf_path)
    collection.add(
        ids=[f"chunk_{i}" for i in range(len(chunks))],
        documents=[c["text"] for c in chunks],
        metadatas=[{"page": c["page"]} for c in chunks],
    )
    return len(chunks)

def search(question, n=3):
    """Return the n chunks most similar in meaning to the question."""
    results = collection.query(query_texts=[question], n_results=n)
    found = []
    for text, meta in zip(results["documents"][0], results["metadatas"][0]):
        found.append({"page": meta["page"], "text": text})
    return found

if __name__ == "__main__":
    if collection.count() == 0:
        print("Indexed", build_index("docs/sample.pdf"), "chunks")
    else:
        print("Already indexed:", collection.count(), "chunks")

    for r in search("What is self-attention?"):
        print(f"\n--- page {r['page']} ---")
        print(r["text"][:300])