"""Sentence-transformer embedding wrapper."""
from __future__ import annotations

import os
from functools import lru_cache
from typing import Sequence

MODEL_NAME = os.getenv("EPFOSATHI_EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")


@lru_cache(maxsize=1)
def get_model():
    # Lazy import keeps chunking and its unit tests lightweight.
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer(MODEL_NAME)


def embed_texts(texts: Sequence[str]) -> list[list[float]]:
    if not texts:
        return []
    vectors = get_model().encode(
        list(texts),
        normalize_embeddings=True,
        convert_to_numpy=True,
        show_progress_bar=len(texts) > 20,
    )
    return vectors.tolist()


def embed_query(query: str) -> list[float]:
    if not query or not query.strip():
        raise ValueError("Query must not be empty.")
    return embed_texts([query.strip()])[0]
