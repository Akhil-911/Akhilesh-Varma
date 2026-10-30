from pypdf import PdfReader

def load_pdf(path):
    """Read a PDF and return a list of {page, text}."""
    reader = PdfReader(path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        pages.append({"page": i + 1, "text": text})
    return pages

def chunk_text(text, chunk_size=800, overlap=150):
    """Split text into overlapping pieces of about chunk_size characters."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start = end - overlap
    return chunks

def build_chunks(pdf_path):
    """Return a list of {page, text} chunks for the whole PDF."""
    chunks = []
    for p in load_pdf(pdf_path):
        for piece in chunk_text(p["text"]):
            if piece.strip():
                chunks.append({"page": p["page"], "text": piece})
    return chunks

if __name__ == "__main__":
    chunks = build_chunks("docs/sample.pdf")
    print(f"Total chunks: {len(chunks)}")
    print(chunks[0])