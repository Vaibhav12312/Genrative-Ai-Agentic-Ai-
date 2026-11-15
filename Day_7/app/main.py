"""FastAPI application exposing EPFOSathi semantic search."""
from fastapi import FastAPI, HTTPException, Query

from app.vectorstore import semantic_search, get_collection

app = FastAPI(
    title="EPFOSathi Semantic Search API",
    version="1.0.0",
    description="Semantic retrieval over source-traceable EPFO FAQ and document chunks.",
)


@app.get("/health")
def health():
    try:
        count = get_collection().count()
        return {"status": "ok", "collection": "epfosathi_documents", "indexed_chunks": count}
    except Exception as exc:
        return {"status": "not_ready", "detail": str(exc)}


@app.get("/search/semantic")
def search_semantic(
    q: str = Query(..., min_length=3, description="Natural-language EPFO question"),
    k: int = Query(5, ge=1, le=20, description="Number of chunks to return"),
):
    try:
        results = semantic_search(q, k=k)
        return {"query": q, "count": len(results), "results": results}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Semantic search failed: {exc}") from exc
