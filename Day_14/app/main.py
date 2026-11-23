from __future__ import annotations

import hashlib
import json
import logging
import time
from contextlib import asynccontextmanager
from datetime import date
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

from app.agent import search_knowledge_base
from app.database import create_record, init_db, list_records, search_records
from app.services import datetools
from app.services.cache import TTLCache
from app.services.llm import FakeLLM, estimate_tokens

logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger("epfosathi")
@asynccontextmanager
async def lifespan(_app: FastAPI):
    init_db()
    yield


app = FastAPI(
    title="EPFOSathi API", version="1.0.0",
    description="EPFO information assistant demo", lifespan=lifespan
)
cache = TTLCache(max_entries=128, ttl_seconds=60)
llm = FakeLLM()
MAX_QUESTION_CHARS = 4_000
MAX_TITLE_CHARS = 160
MAX_CONTENT_CHARS = 8_000


class AskRequest(BaseModel):
    question: str = Field(min_length=1, max_length=MAX_QUESTION_CHARS)


class RecordCreate(BaseModel):
    title: str = Field(min_length=1, max_length=MAX_TITLE_CHARS)
    content: str = Field(min_length=1, max_length=MAX_CONTENT_CHARS)
    category: str = Field(default="general", min_length=1, max_length=80)


@app.middleware("http")
async def request_observability(request: Request, call_next):
    started = time.perf_counter()
    response = await call_next(request)
    latency_ms = round((time.perf_counter() - started) * 1000, 2)
    response.headers["X-Process-Time-ms"] = str(latency_ms)
    logger.info(json.dumps({
        "event": "http_request", "method": request.method,
        "path": request.url.path, "status_code": response.status_code,
        "latency_ms": latency_ms,
    }))
    return response


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return """<!doctype html><html><head><title>EPFOSathi</title>
    <meta name='viewport' content='width=device-width, initial-scale=1'>
    <style>body{font:16px system-ui;max-width:760px;margin:50px auto;padding:0 20px;color:#17324d}
    textarea{width:100%;min-height:110px;padding:12px}button{padding:10px 18px;background:#145da0;color:white;border:0;border-radius:6px}
    pre{white-space:pre-wrap;background:#f2f6fa;padding:16px;border-radius:8px}</style></head>
    <body><h1>EPFOSathi</h1><p>Your simple guide to general EPFO and provident-fund information.</p>
    <textarea id='q' maxlength='4000' placeholder='Ask a general EPFO question...'></textarea><p>
    <button onclick='ask()'>Ask EPFOSathi</button></p><pre id='answer'>Your answer will appear here.</pre>
    <p><a href='/docs'>API documentation</a> · <a href='/health'>Health</a></p>
    <script>async function ask(){const q=document.getElementById('q').value;const out=document.getElementById('answer');
    out.textContent='Thinking...';try{const r=await fetch('/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q})});
    const d=await r.json();out.textContent=r.ok?d.answer:(d.detail||'Request failed');}catch(e){out.textContent='Unable to reach the API.';}}</script></body></html>"""


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "EPFOSathi"}


@app.get("/records")
def records(limit: Annotated[int, Query(ge=1, le=100)] = 100):
    items = list_records(limit)
    return {"items": items, "count": len(items)}


@app.post("/records", status_code=201)
def add_record(payload: RecordCreate):
    return create_record(payload.title.strip(), payload.content.strip(), payload.category.strip())


@app.get("/search")
def search(q: Annotated[str, Query(min_length=1, max_length=200)]):
    items = search_records(q.strip())
    return {"items": items, "count": len(items)}


@app.post("/ask")
def ask(payload: AskRequest):
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=422, detail="Question cannot be blank.")
    key = hashlib.sha256(question.casefold().encode("utf-8")).hexdigest()
    cached = cache.get(key)
    cache_hit = cached is not None
    started = time.perf_counter()
    if cache_hit:
        answer = cached
        context = ""
    else:
        matches = search_knowledge_base(question)
        context = "\n".join(str(item["content"]) for item in matches)
        answer = llm.generate(question, context)
        cache.set(key, answer)
    latency_ms = round((time.perf_counter() - started) * 1000, 2)
    input_tokens = estimate_tokens(question + context + "SYSTEM_PROMPT")
    output_tokens = estimate_tokens(answer)
    logger.info(json.dumps({
        "event": "llm_request", "latency_ms": latency_ms,
        "input_tokens_est": input_tokens, "output_tokens_est": output_tokens,
        "total_tokens_est": input_tokens + output_tokens, "cache_hit": cache_hit,
    }))
    return {
        "answer": answer,
        "usage": {"input_tokens_est": input_tokens, "output_tokens_est": output_tokens,
                  "total_tokens_est": input_tokens + output_tokens},
        "latency_ms": latency_ms,
        "cache": "hit" if cache_hit else "miss",
        "safety_note": "General information only; use official EPFO channels for account-specific actions.",
    }


@app.get("/tools/date-rule")
def date_rule(
    rule: Annotated[str, Query(pattern="^(inoperative|withdrawal|option)$")],
    on: date,
    dob: date | None = None,
):
    """Deterministic date calculations (never computed by the LLM)."""
    if rule == "inoperative":
        if dob is None:
            raise HTTPException(status_code=422, detail="dob is required for this rule.")
        return datetools.inoperative_date(on, dob)
    if rule == "withdrawal":
        return {"eligible_on": datetools.withdrawal_eligible_on(on), "verify": True}
    return {"deadline": datetools.option_deadline(on), "verify": True}
