"""Check EPFOSathi submission files and unfinished evaluation placeholders."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "app/llm.py", "app/main.py", "app/chat.py", "app/schemas.py",
    "prompts/system.md", "prompts/task_v1.md", "prompts/task_v2.md",
    "eval/questions.json", "eval/run_eval.py", "eval/prompt_compare.md",
    ".env.example", ".gitignore",
]
PLACEHOLDERS = re.compile(
    r"Not run yet|fill in (?:by hand|after)|write after scoring|_v1 / v2_|"
    r"_e\.g\.|\|\s*\|\s*\|\s*\|"
    , re.IGNORECASE
)


def main() -> int:
    errors: list[str] = []
    missing = [p for p in REQUIRED if not (ROOT / p).is_file()]
    if missing:
        errors.append("Missing required files: " + ", ".join(missing))

    env_example = ROOT / ".env.example"
    if env_example.exists() and not (ROOT / ".gitignore").exists():
        errors.append(".gitignore is missing")
    if (ROOT / ".env").exists():
        errors.append("A real .env file exists; do not include secrets in the submission")

    questions_path = ROOT / "eval/questions.json"
    if questions_path.exists():
        try:
            questions = json.loads(questions_path.read_text(encoding="utf-8"))
            if len(questions) != 10:
                errors.append(f"Expected 10 evaluation questions; found {len(questions)}")
            q6 = next((q for q in questions if q.get("id") == 6), None)
            if not q6 or q6.get("type") != "personal-data-unavailable":
                errors.append("Q6 must test a personal EPF detail unavailable to the app's data")
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"Could not read eval/questions.json: {exc}")

    comparison_path = ROOT / "eval/prompt_compare.md"
    if comparison_path.exists():
        comparison = comparison_path.read_text(encoding="utf-8")
        if "Question-by-question comparison" not in comparison:
            errors.append("eval/prompt_compare.md must include a question-by-question comparison")
        if "Q10" not in comparison or "Q6" not in comparison:
            errors.append("Prompt comparison must explicitly cover all 10 questions, including Q6")

    scan_files = [ROOT / "README.md", ROOT / "eval/prompt_compare.md"]
    placeholder_hits = []
    for path in scan_files:
        if path.exists():
            for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                if PLACEHOLDERS.search(line):
                    placeholder_hits.append(f"{path.relative_to(ROOT)}:{line_no}: {line.strip()}")
    if placeholder_hits:
        errors.append("Unfinished placeholders found:\n  " + "\n  ".join(placeholder_hits))

    print("EPFOSathi submission check")
    print("TODO / placeholder lines: " + ("none found" if not placeholder_hits else "found"))
    if errors:
        for error in errors:
            print("BLOCKER: " + error)
        return 1
    print("All required submission checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
