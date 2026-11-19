"""SQLite-backed EPF/EPFO knowledge records."""
from __future__ import annotations

import os
import re
import sqlite3
from pathlib import Path
from typing import Any

DEFAULT_RECORDS = [
    {"id": "UAN-001", "title": "What is a Universal Account Number (UAN)?", "category": "UAN", "content": "UAN is a 12-digit number allotted by EPFO. It acts as a single identifier for a member across multiple Member IDs linked to different employers. Keep it confidential and use official EPFO channels for account actions."},
    {"id": "KYC-001", "title": "How do I update KYC details?", "category": "KYC", "content": "Members can sign in to the official EPFO member portal and use the Manage section to submit eligible KYC details. Aadhaar, PAN and bank details may require verification by the relevant authority or employer. Never share OTPs or passwords."},
    {"id": "CLAIM-001", "title": "How can I check a PF claim?", "category": "Claims", "content": "A member can check claim status through the official EPFO member portal or UMANG app. Keep the UAN and registered mobile available. Processing times can vary; rely on the official portal for current status."},
    {"id": "PASSBOOK-001", "title": "Where can I view my EPF passbook?", "category": "Passbook", "content": "Eligible members can access the EPF passbook through the EPFO passbook portal using their member credentials. Passbook availability may be delayed for some exempted establishments or during service interruptions."},
    {"id": "TRANSFER-001", "title": "How do I transfer PF when changing jobs?", "category": "Transfer", "content": "When changing jobs, members can generally submit an online transfer request through the EPFO member portal, subject to eligibility and KYC requirements. Verify employer and member details before submitting."},
    {"id": "GRIEVANCE-001", "title": "How do I raise an EPFO grievance?", "category": "Grievance", "content": "Members can lodge and track a complaint using the official EPFiGMS grievance portal. Include relevant reference details, avoid sharing passwords or OTPs, and retain the grievance registration number."},
]

class RecordStore:
    def __init__(self, db_path: str | None = None):
        self.db_path = db_path or os.getenv("EPFOSATHI_DB", "./data/epfosathi.db")
        if self.db_path != ":memory:":
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.execute("CREATE TABLE IF NOT EXISTS records (id TEXT PRIMARY KEY, title TEXT NOT NULL, category TEXT NOT NULL, content TEXT NOT NULL)")
            count = conn.execute("SELECT COUNT(*) FROM records").fetchone()[0]
            if count == 0:
                conn.executemany("INSERT INTO records(id,title,category,content) VALUES(:id,:title,:category,:content)", DEFAULT_RECORDS)

    def list_records(self) -> list[dict[str, Any]]:
        with self._connect() as conn:
            rows = conn.execute("SELECT id,title,category,content FROM records ORDER BY id").fetchall()
        return [dict(row) for row in rows]

    def get_record(self, record_id: str) -> dict[str, Any] | None:
        with self._connect() as conn:
            row = conn.execute("SELECT id,title,category,content FROM records WHERE id=?", (record_id,)).fetchone()
        return dict(row) if row else None

    def search(self, query: str, limit: int = 10) -> list[dict[str, Any]]:
        query = query.strip()
        if not query:
            return []
        stop_words = {"a", "an", "and", "are", "can", "do", "for", "how", "i", "in", "is", "it", "my", "of", "the", "to", "what", "when", "where", "which", "with"}
        terms = [term for term in re.findall(r"[a-zA-Z0-9]+", query) if term.lower() not in stop_words]
        if not terms:
            terms = query.split()
        where = " AND ".join("(title LIKE ? OR category LIKE ? OR content LIKE ?)" for _ in terms)
        params = [value for term in terms for value in (f"%{term}%",) * 3]
        params.append(max(1, min(limit, 50)))
        with self._connect() as conn:
            rows = conn.execute(f"SELECT id,title,category,content FROM records WHERE {where} ORDER BY id LIMIT ?", params).fetchall()
        return [dict(row) for row in rows]
