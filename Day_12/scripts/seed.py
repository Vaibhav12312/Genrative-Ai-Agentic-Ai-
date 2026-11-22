"""Load the bundled EPFOSathi starter records into the configured database."""

import json
from pathlib import Path

from app.database import init_db
from app.repository import create_record
from app.schemas import RecordCreate

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    init_db()
    seed_file = ROOT / "data" / "seed.json"
    items = json.loads(seed_file.read_text(encoding="utf-8"))
    for item in items:
        create_record(RecordCreate(**item))
    print(f"Seed complete: {len(items)} starter records checked (safe to rerun).")


if __name__ == "__main__":
    main()
