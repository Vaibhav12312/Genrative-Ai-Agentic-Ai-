"""Run the 15-question offline evaluation for two retrieval configurations."""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.rag import EpfosathiRAG, ABSTENTION

EVAL_FILE = ROOT / "eval" / "eval_set.json"
DOCS_FILE = ROOT / "data" / "source_docs.json"


def evaluate(chunk_size: int, top_k: int) -> dict:
    rag = EpfosathiRAG(DOCS_FILE, chunk_size=chunk_size, top_k=top_k)
    rows = json.loads(EVAL_FILE.read_text(encoding="utf-8"))
    if len(rows) != 15:
        raise ValueError(f"Expected exactly 15 evaluation rows, found {len(rows)}")
    q6_rows = [row for row in rows if row["id"] == "Q6"]
    if len(q6_rows) != 1 or not q6_rows[0]["must_abstain"]:
        raise ValueError("Evaluation set must contain exactly one abstaining Q6 row")

    passed = 0
    citation_ok = 0
    abstain_ok = 0
    details = []
    for row in rows:
        result = rag.answer(row["question"], row["id"])
        if row["must_abstain"]:
            correct = result["answer"] == ABSTENTION
            abstain_ok += int(correct)
        else:
            answer_l = result["answer"].lower()
            has_expected_content = all(
                keyword.lower() in answer_l for keyword in row["expected_keywords"]
            )
            has_citation = bool(result["citations"])
            citation_ok += int(has_citation)
            # An answerable row only passes when it is both grounded and cited.
            correct = has_expected_content and has_citation
        passed += int(correct)
        details.append({"id": row["id"], "passed": correct})
    total = len(rows)
    answerable_total = sum(not row["must_abstain"] for row in rows)
    return {
        "chunk_size": chunk_size,
        "top_k": top_k,
        "passed": passed,
        "total": total,
        "accuracy_pct": round(100 * passed / total, 1),
        "citation_coverage": f"{citation_ok}/{answerable_total}",
        "q6_abstention": f"{abstain_ok}/1",
        "details": details,
    }


def main():
    configs = [(250, 2), (450, 4)]
    results = [evaluate(*cfg) for cfg in configs]
    # Prefer higher pass count, then citation coverage, then smaller top-k.
    winner = sorted(
        results,
        key=lambda r: (
            r["passed"],
            int(r["citation_coverage"].split("/")[0]),
            -r["top_k"],
        ),
        reverse=True,
    )[0]
    print("CONFIGURATION RESULTS")
    print("| Chunk size | Top-k | Passed | Accuracy | Citation coverage | Q6 abstention |")
    print("|---:|---:|---:|---:|---:|---:|")
    for r in results:
        print(f'| {r["chunk_size"]} | {r["top_k"]} | {r["passed"]}/{r["total"]} | '
              f'{r["accuracy_pct"]:.1f}% | {r["citation_coverage"]} | {r["q6_abstention"]} |')
    print(f'\nWinner: chunk_size={winner["chunk_size"]}, top_k={winner["top_k"]}')
    print("\nPer-question results:")
    for r in results:
        failed = [d["id"] for d in r["details"] if not d["passed"]]
        print(f'  ({r["chunk_size"]}, {r["top_k"]}): failed={failed or "none"}')


if __name__ == "__main__":
    main()
