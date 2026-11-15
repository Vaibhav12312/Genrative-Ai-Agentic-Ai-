"""Persistent Chroma index for EPFOSathi document chunks."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

from app.chunking import build_chunks
from app.embed import embed_query, embed_texts

PROJECT_DIR = Path(__file__).resolve().parents[1]
CHROMA_PATH = Path(os.getenv("EPFOSATHI_CHROMA_PATH", str(PROJECT_DIR / "chroma_db")))
COLLECTION_NAME = os.getenv("EPFOSATHI_COLLECTION", "epfosathi_documents")


def _client():
    # Import Chroma lazily so chunking, API contract tests, and documentation
    # tooling can run without loading the optional vector database at import time.
    import chromadb

    CHROMA_PATH.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_PATH))


def get_collection():
    return _client().get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine", "description": "EPFOSathi source document chunks"},
    )


def index_chunks(chunks: list[dict[str, Any]], rebuild: bool = False) -> int:
    client = _client()
    if rebuild:
        try:
            client.delete_collection(COLLECTION_NAME)
        except Exception:
            pass
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine", "description": "EPFOSathi source document chunks"},
    )
    if not chunks:
        raise ValueError("No chunks were produced; check your source documents.")
    batch_size = 64
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]
        vectors = embed_texts([item["text"] for item in batch])
        metadatas = []
        for item in batch:
            metadata = {
                "title": item["title"],
                "source": item["source"],
                "document_id": item["document_id"],
                "chunk_index": int(item["chunk_index"]),
            }
            if item.get("page") is not None:
                metadata["page"] = int(item["page"])
            metadatas.append(metadata)
        collection.upsert(
            ids=[item["id"] for item in batch],
            documents=[item["text"] for item in batch],
            metadatas=metadatas,
            embeddings=vectors,
        )
    return collection.count()


def semantic_search(query: str, k: int = 5) -> list[dict[str, Any]]:
    query = query.strip()
    if not query:
        raise ValueError("Query must not be empty.")
    collection = get_collection()
    if collection.count() == 0:
        raise RuntimeError("Chroma collection is empty. Run: python -m app.vectorstore --rebuild")
    result = collection.query(
        query_embeddings=[embed_query(query)],
        n_results=min(k, collection.count()),
        include=["documents", "metadatas", "distances"],
    )
    hits = []
    ids = (result.get("ids") or [[]])[0]
    docs = (result.get("documents") or [[]])[0]
    metas = (result.get("metadatas") or [[]])[0]
    distances = (result.get("distances") or [[]])[0]
    for chunk_id, text, metadata, distance in zip(ids, docs, metas, distances):
        metadata = metadata or {}
        hits.append({
            "id": chunk_id,
            "text": text,
            "title": metadata.get("title"),
            "source": metadata.get("source"),
            "page": metadata.get("page"),
            "document_id": metadata.get("document_id"),
            "chunk_index": metadata.get("chunk_index"),
            "distance": float(distance),
            "similarity": round(1.0 - float(distance), 6),
        })
    return hits


def main():
    parser = argparse.ArgumentParser(description="Build the persistent EPFOSathi Chroma index.")
    parser.add_argument("--rebuild", action="store_true", help="Delete and recreate the collection.")
    args = parser.parse_args()
    chunks = build_chunks()
    count = index_chunks(chunks, rebuild=args.rebuild)
    print(f"Indexed {len(chunks)} chunks. Chroma collection now contains {count} chunks.")
    print(f"Persistent database: {CHROMA_PATH.resolve()}")
    print(f"Collection: {COLLECTION_NAME}")


if __name__ == "__main__":
    main()
