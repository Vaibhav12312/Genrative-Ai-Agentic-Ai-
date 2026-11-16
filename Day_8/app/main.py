from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from app.rag import EpfosathiRAG

app = FastAPI(
    title="EPFOSathi API",
    description="Grounded EPFO member-help answers with source citations.",
    version="1.0.0",
)
rag = EpfosathiRAG(chunk_size=450, top_k=4)


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=2000)
    question_id: str | None = Field(default=None, max_length=20)


class Citation(BaseModel):
    id: str
    title: str
    url: str


class AskResponse(BaseModel):
    answer: str
    citations: list[Citation]
    retrieved_chunks: list[dict]


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest):
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=422, detail="question must not be blank")
    try:
        return rag.answer(question, payload.question_id)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
