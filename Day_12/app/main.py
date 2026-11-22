from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.agent import EPFOAgent
from app.database import init_db
from app.llm import get_llm
from app.repository import create_record, get_record, list_records, search_records
from app.schemas import AskRequest, AskResponse, RecordCreate, RecordOut


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(
    title="EPFOSathi API",
    description="A searchable, source-aware assistant for general EPFO information.",
    version="1.1.0",
    lifespan=lifespan,
)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


@app.get("/", include_in_schema=False)
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/health")
def health():
    return {"status": "ok", "service": "EPFOSathi"}


@app.post("/records", response_model=RecordOut, status_code=201)
def add_record(payload: RecordCreate):
    return create_record(payload)


@app.get("/records", response_model=list[RecordOut])
def get_records(limit: int = Query(default=100, ge=1, le=500),
                offset: int = Query(default=0, ge=0)):
    return list_records(limit, offset)


@app.get("/search", response_model=list[RecordOut])
def search(q: str = Query(min_length=1, max_length=200),
           limit: int = Query(default=10, ge=1, le=100)):
    return search_records(q, limit)


# Day 10/11 browser-client compatibility routes.
@app.get("/api/records")
def legacy_records():
    items = list_records(limit=500)
    return {"records": items, "count": len(items)}


@app.get("/api/records/{record_id}")
def legacy_record_detail(record_id: str):
    item = get_record(record_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return item


@app.get("/api/search")
def legacy_search(q: str = Query(min_length=1, max_length=200),
                  limit: int = Query(default=10, ge=1, le=50)):
    results = search_records(q, limit)
    return {"query": q, "results": results, "count": len(results)}


@app.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest):
    try:
        answer, sources = EPFOAgent(get_llm()).answer(payload.question)
        all_records = list_records(limit=500)
        source_details = [
            {"id": row["id"], "legacy_id": row.get("legacy_id"), "title": row["title"]}
            for row in all_records if row["id"] in sources
        ]
        return AskResponse(
            answer=answer, sources=sources, source_details=source_details
        )
    except Exception as exc:
        raise HTTPException(
            status_code=503, detail="Assistant is temporarily unavailable."
        ) from exc
