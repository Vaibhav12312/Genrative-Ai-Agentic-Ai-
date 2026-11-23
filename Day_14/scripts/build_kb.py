"""Load FAQ records, dedupe them (newest/most authoritative wins) and write data/kb.json."""
from __future__ import annotations

import json
import runpy
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from app.services.dedupe import dedupe  # noqa: E402

records = runpy.run_path(str(ROOT / "data" / "sample_records.py"))["sample_records"]
canonical, review = dedupe(records)
(ROOT / "data" / "kb.json").write_text(json.dumps(
    {"records": canonical, "review_queue": review}, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"{len(records)} in -> {len(canonical)} canonical, {len(review)} need review, "
      f"{sum(r['outdated'] for r in canonical)} flagged outdated")
