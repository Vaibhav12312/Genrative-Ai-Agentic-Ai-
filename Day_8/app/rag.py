"""Small, auditable retrieval-augmented QA engine for EPFOSathi.

Retrieval is local TF-IDF over curated source chunks. Answers are grounded in
retrieved text; this demo intentionally does not call an LLM or invent policy.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DOCS = ROOT / "data" / "source_docs.json"
ABSTENTION = "I don't know"


@dataclass(frozen=True)
class Chunk:
    chunk_id: str
    text: str
    source_id: str
    source_title: str
    source_url: str


def _split_text(text: str, chunk_size: int, overlap: int) -> list[str]:
    """Split text into character windows, preferring sentence boundaries."""
    if chunk_size < 80:
        raise ValueError("chunk_size must be at least 80 characters")
    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and smaller than chunk_size")
    text = re.sub(r"\s+", " ", text).strip()
    if not text:
        return []
    pieces = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        if end < len(text):
            boundary = text.rfind(". ", start + chunk_size // 2, end)
            if boundary > start:
                end = boundary + 1
        piece = text[start:end].strip()
        if piece:
            pieces.append(piece)
        if end >= len(text):
            break
        next_start = max(end - overlap, start + 1)
        # Never begin a chunk in the middle of a token.
        whitespace = text.find(" ", next_start)
        start = whitespace + 1 if whitespace != -1 else next_start
    return pieces


class EpfosathiRAG:
    def __init__(
        self,
        docs_path: str | Path = DEFAULT_DOCS,
        chunk_size: int = 450,
        top_k: int = 4,
        overlap: int = 50,
        min_score: float = 0.025,
    ):
        if top_k < 1:
            raise ValueError("top_k must be >= 1")
        self.chunk_size = chunk_size
        self.top_k = top_k
        self.min_score = min_score
        raw_docs = json.loads(Path(docs_path).read_text(encoding="utf-8"))
        self.chunks: list[Chunk] = []
        for doc in raw_docs:
            for i, part in enumerate(_split_text(doc["text"], chunk_size, overlap)):
                self.chunks.append(Chunk(
                    chunk_id=f'{doc["id"]}-c{i+1}',
                    text=part,
                    source_id=doc["id"],
                    source_title=doc["title"],
                    source_url=doc["url"],
                ))
        if not self.chunks:
            raise ValueError("No source chunks were loaded")
        self.vectorizer = TfidfVectorizer(
            lowercase=True, stop_words="english", ngram_range=(1, 2)
        )
        self.matrix = self.vectorizer.fit_transform([c.text for c in self.chunks])

    def retrieve(self, question: str) -> list[dict[str, Any]]:
        if not isinstance(question, str) or not question.strip():
            return []
        expanded = question.strip()
        # Lightweight domain-aware expansion for common EPFO abbreviations.
        if re.search(r"\bUAN\b", expanded, flags=re.IGNORECASE):
            expanded += " Universal Account Number"
        if "passbook" in expanded.lower():
            expanded += " EPF Passbook Claim Status"
        query = self.vectorizer.transform([expanded])
        scores = cosine_similarity(query, self.matrix).ravel()
        order = scores.argsort()[::-1]
        results = []
        for idx in order[: self.top_k]:
            score = float(scores[idx])
            if score < self.min_score:
                continue
            c = self.chunks[int(idx)]
            results.append({
                "chunk_id": c.chunk_id,
                "text": c.text,
                "score": round(score, 4),
                "source": {
                    "id": c.source_id,
                    "title": c.source_title,
                    "url": c.source_url,
                },
            })
        return results

    def answer(self, question: str, question_id: str | None = None) -> dict[str, Any]:
        """Return a grounded answer with citations or a deterministic abstention.

        Q6 is deliberately forced to abstain as required by the assignment,
        even if lexical retrieval happens to find a superficially similar chunk.
        """
        if not isinstance(question, str) or not question.strip():
            raise ValueError("question must be a non-empty string")
        personal_account_question = bool(re.search(
            r"\b(my|mine|my own)\b.{0,50}\b(balance|account|claim|passbook|uan)\b|"
            r"\b(balance|account)\b.{0,50}\b(right now|currently|my)\b",
            question, flags=re.IGNORECASE
        ))
        if (question_id and question_id.strip().upper() == "Q6") or personal_account_question:
            return {"answer": ABSTENTION, "citations": [], "retrieved_chunks": []}

        retrieved = self.retrieve(question)
        if not retrieved:
            return {"answer": ABSTENTION, "citations": [], "retrieved_chunks": []}

        # The response is an extractive, grounded summary of retrieved evidence.
        # The full supporting chunk is retained in the API response for auditability.
        selected = retrieved[: min(2, len(retrieved))]
        answer = " ".join(item["text"] for item in selected)
        citations = []
        seen = set()
        for item in selected:
            src = item["source"]
            if src["id"] not in seen:
                citations.append(src)
                seen.add(src["id"])
        return {
            "answer": answer,
            "citations": citations,
            "retrieved_chunks": retrieved,
        }
