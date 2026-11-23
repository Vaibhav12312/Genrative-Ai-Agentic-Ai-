from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterator

DB_PATH = Path(os.getenv("EPFOSATHI_DB", "./data/epfosathi.db"))


@contextmanager
def connect() -> Iterator[sqlite3.Connection]:
    """Yield a database connection and always close it after the transaction.

    sqlite3.Connection's own context manager handles commit/rollback but does not
    close the connection. Explicit closure is important on Windows, where an open
    connection can prevent temporary database files from being deleted.
    """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    try:
        with connection:
            yield connection
    finally:
        connection.close()


def init_db() -> None:
    with connect() as conn:
        conn.execute(
            """CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'general',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )"""
        )


def create_record(title: str, content: str, category: str = "general") -> dict[str, Any]:
    with connect() as conn:
        cursor = conn.execute(
            "INSERT INTO records(title, content, category) VALUES (?, ?, ?)",
            (title, content, category),
        )
        row = conn.execute("SELECT * FROM records WHERE id = ?", (cursor.lastrowid,)).fetchone()
        return dict(row)


def list_records(limit: int = 100) -> list[dict[str, Any]]:
    with connect() as conn:
        rows = conn.execute(
            "SELECT * FROM records ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
        return [dict(row) for row in rows]


def search_records(query: str, limit: int = 20) -> list[dict[str, Any]]:
    needle = f"%{query}%"
    with connect() as conn:
        rows = conn.execute(
            """SELECT * FROM records
               WHERE title LIKE ? OR content LIKE ? OR category LIKE ?
               ORDER BY id DESC LIMIT ?""",
            (needle, needle, needle, limit),
        ).fetchall()
        return [dict(row) for row in rows]
