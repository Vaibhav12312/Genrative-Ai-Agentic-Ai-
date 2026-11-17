"""Transparent lexical RAG retrieval over data/source_docs.json."""
import json
import re
from pathlib import Path
from typing import Any

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "source_docs.json"
STOPWORDS = {
    "a", "an", "and", "are", "can", "do", "does", "for", "from", "how",
    "i", "in", "is", "it", "me", "my", "of", "on", "or", "should", "the",
    "to", "what", "when", "where", "which", "why", "with", "you", "your",
}


def _tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS]


def load_documents(path: Path = DATA_PATH) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        docs = json.load(handle)
    if not isinstance(docs, list):
        raise ValueError("source_docs.json must contain a JSON list")
    for index, doc in enumerate(docs):
        if not all(key in doc for key in ("source_id", "title", "text")):
            raise ValueError(f"Document at index {index} is missing required fields")
    return docs


def search_chunks(question: str, top_k: int = 4, chunk_size: int = 450) -> list[dict[str, Any]]:
    if not question or not question.strip():
        return []
    if top_k < 1:
        raise ValueError("top_k must be at least 1")
    if chunk_size < 1:
        raise ValueError("chunk_size must be at least 1")
    query_tokens = _tokens(question)
    if not query_tokens:
        return []
    query = set(query_tokens)
    scored = []
    for doc in load_documents():
        text = doc["text"]
        title_tokens = set(_tokens(doc["title"]))
        body_tokens = set(_tokens(text))
        overlap = len(query & body_tokens)
        title_overlap = len(query & title_tokens)
        if overlap or title_overlap:
            # Title matches receive a modest boost; score remains explainable.
            score = (overlap + 1.5 * title_overlap) / len(query)
            scored.append((score, doc))
    scored.sort(key=lambda item: (-item[0], item[1]["source_id"]))
    return [{
        "text": doc["text"][:chunk_size],
        "source_id": doc["source_id"],
        "title": doc["title"],
        "score": round(score, 4),
        "citation": f'[{doc["source_id"]}]',
    } for score, doc in scored[:top_k]]


def format_citations(chunks: list[dict[str, Any]]) -> str:
    return " ".join(dict.fromkeys(chunk["citation"] for chunk in chunks))
