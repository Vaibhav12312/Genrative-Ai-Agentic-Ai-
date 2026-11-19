from __future__ import annotations
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from .agent import EPFAgent
from .records import RecordStore

BASE_DIR = Path(__file__).resolve().parent
store = RecordStore()
agent = EPFAgent(store)
app = FastAPI(title="EPFOSathi API", version="1.0.0", description="A grounded EPF/EPFO information assistant.")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")

class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=1000)

@app.get("/", include_in_schema=False)
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")

@app.get("/health")
def health():
    return {"status": "ok", "service": "EPFOSathi", "records": len(store.list_records())}

@app.get("/api/records")
def records():
    return {"records": store.list_records(), "count": len(store.list_records())}

@app.get("/api/records/{record_id}")
def record_detail(record_id: str):
    item = store.get_record(record_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return item

@app.get("/api/search")
def search(q: str = Query(min_length=1, max_length=200), limit: int = Query(default=10, ge=1, le=50)):
    matches = store.search(q, limit)
    return {"query": q, "results": matches, "count": len(matches)}

@app.post("/ask")
def ask(payload: AskRequest):
    return agent.ask(payload.question)
