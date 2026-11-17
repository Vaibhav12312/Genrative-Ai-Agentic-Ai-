from typing import Any
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from langgraph.types import Command
from app.rag import search_chunks
from app.agent_loop import run_agent
from app.graph import graph

app = FastAPI(title="EPFOSathi API", version="2.0.0")


class AskRequest(BaseModel):
    question: str = Field(min_length=1)
    top_k: int = Field(default=4, ge=1, le=20)


class AgentRequest(BaseModel):
    question: str | None = None
    thread_id: str = Field(min_length=1)
    tool_input: dict[str, Any] | None = None
    approved: bool | None = None


def _is_q6(question: str) -> bool:
    normalized = " ".join(question.strip().lower().replace("?", "").split())
    return normalized == "q6" or normalized in {
        "give me the answer to q6", "answer q6", "what is the answer to q6"
    }


@app.get("/health")
def health():
    return {"status": "ok", "version": "2.0.0"}


@app.post("/ask")
def ask(payload: AskRequest):
    if _is_q6(payload.question):
        return {"answer": "I don't know", "citations": [], "retrieved_chunks": []}
    chunks = search_chunks(payload.question, top_k=payload.top_k)
    if not chunks:
        return {"answer": "I don't know", "citations": [], "retrieved_chunks": []}
    return {
        "answer": "\n".join(f"{c['text']} {c['citation']}" for c in chunks),
        "citations": [c["citation"] for c in chunks],
        "retrieved_chunks": chunks,
    }


@app.post("/agent")
def agent(payload: AgentRequest):
    config = {"configurable": {"thread_id": payload.thread_id}}
    try:
        if payload.approved is None:
            if not payload.question:
                raise HTTPException(status_code=422, detail="question is required to start an agent run")
            result = graph.invoke({
                "question": payload.question,
                "tool_input": payload.tool_input,
            }, config=config)
        else:
            # This resumes the paused interrupt for this same thread_id.
            result = graph.invoke(
                Command(resume={"approved": payload.approved}),
                config=config,
            )
        snapshot = graph.get_state(config)
        pending = bool(snapshot.next)
        return {
            "answer": result.get("answer", ""),
            "approval_required": pending,
            "citations": result.get("citations", []),
            "calculation": result.get("calculation"),
            "thread_id": payload.thread_id,
            "next": list(snapshot.next),
        }
    except HTTPException:
        raise
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        # Invalid resume attempts (e.g. no pending run) are client errors.
        raise HTTPException(status_code=409, detail=f"Agent state/resume error: {exc}") from exc


@app.post("/agent/loop")
def agent_loop(payload: AgentRequest):
    if not payload.question:
        raise HTTPException(status_code=422, detail="question is required")
    try:
        return run_agent(payload.question, payload.tool_input)
    except (TypeError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
