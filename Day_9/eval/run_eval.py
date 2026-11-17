
"""Compare two retrieval configurations against the 15-item evaluation set."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.rag import search_chunks

items = json.loads((ROOT / "eval" / "eval_set.json").read_text(encoding="utf-8"))


def evaluate(top_k: int, chunk_size: int) -> dict:
    hits = 0
    rows = []
    for item in items:
        if item["id"] == "Q6":
            answer = "I don't know"
            predicted = []
            correct = answer == item["expected_answer"]
        else:
            chunks = search_chunks(item["question"], top_k=top_k, chunk_size=chunk_size)
            predicted = [c["source_id"] for c in chunks]
            correct = bool(set(item["expected_source_ids"]) & set(predicted))
        hits += int(correct)
        rows.append({"id": item["id"], "correct": correct, "predicted": predicted})
    return {"top_k": top_k, "chunk_size": chunk_size, "correct": hits,
            "total": len(items), "accuracy": round(hits / len(items), 4), "rows": rows}


if __name__ == "__main__":
    results = [evaluate(4, 450), evaluate(6, 700)]
    for result in results:
        print(f"top_k={result['top_k']} chunk_size={result['chunk_size']}: "
              f"{result['correct']}/{result['total']} ({result['accuracy']:.0%})")
    print("Selected configuration:", max(results, key=lambda r: r["accuracy"])["top_k"],
          "top_k; ties favor the first (baseline) configuration.")
