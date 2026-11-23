from __future__ import annotations

from app.database import search_records


def search_knowledge_base(query: str) -> list[dict[str, object]]:
    """Agent tool: retrieve matching locally stored knowledge records."""
    return search_records(query, limit=5)
