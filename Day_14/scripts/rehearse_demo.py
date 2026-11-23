"""Run two repeatable API-level EPFOSathi demo walkthroughs.

This is an automated smoke rehearsal, not a substitute for a human browser demo.
Run from the repository root: python scripts/rehearse_demo.py
"""
from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient  # noqa: E402

from app import database, main  # noqa: E402


def run_rehearsal(number: int) -> None:
    with tempfile.TemporaryDirectory(prefix="epfosathi-demo-") as tmp:
        database.DB_PATH = Path(tmp) / "demo.db"
        main.cache.clear()
        main.llm.calls = 0

        with TestClient(main.app) as client:
            checks: list[tuple[str, bool]] = []
            checks.append(("home page", client.get("/").status_code == 200))
            health = client.get("/health")
            checks.append(("health endpoint", health.status_code == 200 and health.json().get("status") == "ok"))

            answer = client.post("/ask", json={"question": "What is a Universal Account Number (UAN)?"})
            checks.append(("FAQ question", answer.status_code == 200 and bool(answer.json().get("answer"))))

            date_result = client.get(
                "/tools/date-rule", params={"rule": "withdrawal", "on": "2026-01-15"}
            )
            checks.append(("deterministic date tool", date_result.status_code == 200
                           and date_result.json().get("eligible_on") == "2026-03-15"))

            invalid = client.get("/tools/date-rule", params={"rule": "inoperative", "on": "2026-01-15"})
            checks.append(("missing-input validation", invalid.status_code == 422))

        failed = [name for name, passed in checks if not passed]
        print(f"Rehearsal {number}: " + ", ".join(
            f"{name}={'PASS' if passed else 'FAIL'}" for name, passed in checks
        ))
        if failed:
            raise SystemExit(f"Rehearsal {number} failed: {', '.join(failed)}")


if __name__ == "__main__":
    run_rehearsal(1)
    run_rehearsal(2)
    print("Both API-level smoke rehearsals passed. Complete the manual browser demo before interview.")
