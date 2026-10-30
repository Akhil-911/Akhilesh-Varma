from fastapi import FastAPI
from pydantic import BaseModel
from rag import answer

app = FastAPI(title="Document Q&A API")

class Question(BaseModel):
    question: str

@app.get("/")
def health():
    return {"status": "ok"}

@app.post("/ask")
def ask(body: Question):
    text, pages = answer(body.question)
    return {"answer": text, "pages": pages}