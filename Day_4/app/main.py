
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from app.smart_search import load_records, search_records


app = FastAPI(
    title="EPFOSathi API",
    description="EPFO FAQ service with intelligent search",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str = Field(
        ...,
        min_length=2,
        description="Enter your EPFO-related question"
    )


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "EPFOSathi API"
    }


@app.get("/records")
def get_records(limit: int = Query(default=10, ge=1, le=100)):
    records = load_records()

    return {
        "total": len(records),
        "returned": len(records[:limit]),
        "records": records[:limit]
    }


@app.get("/records/{record_id}")
def get_record(record_id: str):
    records = load_records()

    for record in records:
        if record["faq_number"] == record_id:
            return record

    raise HTTPException(
        status_code=404,
        detail=f"FAQ record {record_id} not found"
    )


@app.get("/search")
def search(q: str = Query(..., min_length=1)):
    results = search_records(q)

    return {
        "query": q,
        "total_results": len(results),
        "results": results
    }


@app.post("/questions")
def ask_question(request: QuestionRequest):
    results = search_records(request.question)

    return {
        "question": request.question,
        "total_results": len(results),
        "results": results,
        "message": (
            "Relevant EPFO FAQs found."
            if results
            else "No relevant FAQ found."
        )
    }
