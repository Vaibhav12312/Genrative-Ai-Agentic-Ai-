"""EPFOSathi - FastAPI app exposing POST /chat."""
from fastapi import FastAPI, HTTPException

from app.chat import run_chat
from app.config import get_settings
from app.llm import LLMError
from app.schemas import ChatRequest, ChatResponse

app = FastAPI(
    title="EPFOSathi",
    description="A helpful assistant for EPF / EPFO questions (PF, UAN, KYC, claims, pension).",
    version="0.2.0",
)


@app.get("/health")
def health():
    s = get_settings()
    return {"status": "ok", "provider": s.provider}


@app.post("/chat", response_model=ChatResponse)
def chat(req: ChatRequest) -> ChatResponse:
    try:
        response, _ = run_chat(req.message, req.prompt_version)
        return response
    except LLMError as e:
        raise HTTPException(status_code=502, detail=str(e))
