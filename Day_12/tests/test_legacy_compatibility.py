import sqlite3


def test_legacy_frontend_routes(client):
    records = client.get("/api/records")
    assert records.status_code == 200
    assert records.json()["count"] == 0

    client.post("/records", json={
        "title": "UAN activation",
        "content": "Activate UAN using the member portal.",
        "category": "UAN",
        "legacy_id": "UAN-001",
    })
    assert client.get("/api/records/UAN-001").json()["legacy_id"] == "UAN-001"
    assert client.get("/api/search", params={"q": "UAN"}).json()["count"] == 1


def test_migrates_day10_text_id_database(tmp_path, monkeypatch):
    from app.config import settings
    from app.database import init_db
    from app.repository import get_record, list_records

    db_path = tmp_path / "old.db"
    with sqlite3.connect(db_path) as db:
        db.execute(
            "CREATE TABLE records (id TEXT PRIMARY KEY, title TEXT NOT NULL, "
            "category TEXT NOT NULL, content TEXT NOT NULL)"
        )
        db.execute(
            "INSERT INTO records VALUES (?, ?, ?, ?)",
            ("UAN-001", "What is UAN?", "UAN", "UAN is a member identifier."),
        )
    monkeypatch.setattr(settings, "database_path", str(db_path))
    init_db()
    migrated = get_record("UAN-001")
    assert migrated is not None
    assert migrated["legacy_id"] == "UAN-001"
    assert migrated["title"] == "What is UAN?"
    assert len(list_records()) == 1


def test_seed_data_contains_six_original_records():
    import json
    from pathlib import Path

    data = json.loads((Path(__file__).resolve().parents[1] / "data" / "seed.json")
                      .read_text(encoding="utf-8"))
    assert {item["legacy_id"] for item in data} == {
        "UAN-001", "KYC-001", "CLAIM-001",
        "PASSBOOK-001", "TRANSFER-001", "GRIEVANCE-001",
    }
