import sqlite3
from pathlib import Path

from app.config import settings


def connect():
    path = Path(settings.database_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create the current schema and safely migrate the Day 10 text-ID schema."""
    with connect() as db:
        existing = db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='records'"
        ).fetchone()
        if existing:
            columns = {row["name"] for row in db.execute("PRAGMA table_info(records)")}
            # Day 10 used TEXT IDs and had no created_at. Preserve it before
            # creating the Day 12 integer-ID schema.
            if "created_at" not in columns or "id" not in columns:
                db.execute("ALTER TABLE records RENAME TO records_legacy_migration")
                columns = set()
            elif "legacy_id" not in columns:
                db.execute("ALTER TABLE records ADD COLUMN legacy_id TEXT")
        db.execute("""
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                category TEXT NOT NULL DEFAULT 'general',
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                legacy_id TEXT UNIQUE
            )
        """)
        legacy_table = db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' "
            "AND name='records_legacy_migration'"
        ).fetchone()
        if legacy_table:
            legacy_columns = {row["name"] for row in db.execute(
                "PRAGMA table_info(records_legacy_migration)"
            )}
            if {"id", "title", "content", "category"}.issubset(legacy_columns):
                rows = db.execute(
                    "SELECT id, title, content, category "
                    "FROM records_legacy_migration"
                ).fetchall()
                for row in rows:
                    db.execute(
                        "INSERT OR IGNORE INTO records "
                        "(title, content, category, legacy_id) VALUES (?, ?, ?, ?)",
                        (row["title"], row["content"], row["category"], str(row["id"])),
                    )
            db.execute("DROP TABLE records_legacy_migration")
        db.commit()
