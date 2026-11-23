"""Run lightweight checks for the EPFOSathi interview handover pack."""
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "interview.md"
README = ROOT / "README.md"
PROGRESS = ROOT / "PROGRESS.md"
FAQ_FILE = ROOT / "data" / "sample_records.py"

required = [
    "60-second pitch",
    "Ten likely interview questions",
    "Hardest-problem story",
    "Demo walkthrough",
    "Rehearsal record",
]
text = DOC.read_text(encoding="utf-8")
missing = [heading for heading in required if heading not in text]
if missing:
    raise SystemExit(f"Missing interview sections: {missing}")
if not all(path.is_file() for path in (README, PROGRESS, FAQ_FILE)):
    raise SystemExit("One or more required handover files are missing")
namespace = runpy.run_path(str(FAQ_FILE))
records = namespace.get("sample_records")
if not isinstance(records, list) or not records:
    raise SystemExit("sample_records must be a non-empty list")
print(f"Handover checks passed; validated {len(records)} FAQ input records.")
