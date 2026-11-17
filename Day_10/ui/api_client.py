"""Backend API and local feedback persistence helpers."""
from __future__ import annotations
import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
import requests


def _as_text(value: Any) -> str:
    if value is None: return ""
    if isinstance(value, str): return value.strip()
    if isinstance(value, (dict, list)): return json.dumps(value, ensure_ascii=False, indent=2)
    return str(value)


def normalize_response(payload: Any) -> tuple[str, list[dict[str, str]]]:
    if isinstance(payload, str): return payload.strip(), []
    if not isinstance(payload, dict): return _as_text(payload), []
    answer = ""
    nested_citations: list[dict[str, str]] = []
    for key in ("answer", "response", "output", "message", "content", "final_answer"):
        candidate = payload.get(key)
        if isinstance(candidate, str) and candidate.strip():
            answer = candidate.strip(); break
    if not answer and isinstance(payload.get("data"), dict):
        answer, nested_citations = normalize_response(payload["data"])
    raw = payload.get("citations", payload.get("sources", payload.get("references", [])))
    if isinstance(raw, (str, dict)): raw = [raw]
    citations = list(nested_citations)
    if isinstance(raw, list):
        for index, item in enumerate(raw, 1):
            if isinstance(item, str): citations.append({"label": item, "url": ""})
            elif isinstance(item, dict):
                url = _as_text(item.get("url") or item.get("source_url") or item.get("link"))
                label = _as_text(item.get("title") or item.get("name") or item.get("label") or item.get("source") or url or f"Source {index}")
                citations.append({"label": label, "url": url})
            else: citations.append({"label": _as_text(item), "url": ""})
    return answer or "The API returned a response, but no recognised answer field was found.", citations


def call_backend(base_url: str, endpoint: str, question: str, history: list[dict[str, str]], token: str = "", timeout: int = 45) -> tuple[str, list[dict[str, str]]]:
    base_url = base_url.strip().rstrip("/")
    if not base_url: raise ValueError("Set the backend base URL in the sidebar or EPFOSATHI_API_URL.")
    if endpoint not in ("ask", "agent"): raise ValueError("Endpoint must be 'ask' or 'agent'.")
    headers = {"Accept": "application/json", "Content-Type": "application/json"}
    if token.strip(): headers["Authorization"] = f"Bearer {token.strip()}"
    body = {"question": question, "query": question, "message": question, "chat_history": history}
    response = requests.post(f"{base_url}/{endpoint}", json=body, headers=headers, timeout=timeout)
    response.raise_for_status()
    try: payload = response.json()
    except ValueError: payload = response.text
    return normalize_response(payload)


def save_feedback(db_path: str | Path, question: str, answer: str, vote: str) -> None:
    if vote not in ("up", "down"): raise ValueError("vote must be 'up' or 'down'")
    path = Path(db_path); path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(path) as conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT NOT NULL,
            question TEXT NOT NULL, answer TEXT NOT NULL,
            vote TEXT NOT NULL CHECK(vote IN ('up','down')))""")
        conn.execute("INSERT INTO feedback(created_at, question, answer, vote) VALUES (?, ?, ?, ?)",
                     (datetime.now(timezone.utc).isoformat(), question, answer, vote))
