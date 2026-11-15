"""Run the fixed ten-question retrieval evaluation and write actual hits to Markdown."""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from app.vectorstore import semantic_search

HERE = Path(__file__).resolve().parent
QUESTIONS_FILE = HERE / "questions.json"
OUTPUT_FILE = HERE / "search_results.md"


def main():
    questions = json.loads(QUESTIONS_FILE.read_text(encoding="utf-8"))
    lines = [
        "# EPFOSathi Semantic Retrieval Evaluation",
        "",
        f"- Run time (UTC): {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
        "- Retrieval method: SentenceTransformer embeddings + persistent Chroma cosine search",
        "- Questions: 10",
        "",
        "> These are runtime results from the current indexed corpus. Review source and page metadata before treating a hit as relevant.",
        "",
    ]
    total_hits = 0
    for item in questions:
        qid, question = item["id"], item["question"]
        hits = semantic_search(question, k=5)
        total_hits += len(hits)
        lines.extend([f"## Q{qid}. {question}", ""])
        if not hits:
            lines.extend(["No hits returned.", ""])
            continue
        for rank, hit in enumerate(hits, start=1):
            page = hit["page"] if hit["page"] is not None else "N/A (source has no page field)"
            excerpt = " ".join(hit["text"].split())
            if len(excerpt) > 360:
                excerpt = excerpt[:357].rstrip() + "..."
            lines.extend([
                f"### Rank {rank}",
                f"- **Title:** {hit['title']}",
                f"- **Source:** {hit['source']}",
                f"- **Page:** {page}",
                f"- **Chunk index:** {hit['chunk_index']}",
                f"- **Distance:** {hit['distance']:.6f}",
                f"- **Similarity (1 - distance):** {hit['similarity']:.6f}",
                f"- **Excerpt:** {excerpt}",
                "",
            ])
    lines.extend([
        "## Run summary",
        "",
        f"- Questions executed: {len(questions)}",
        f"- Total hits recorded: {total_hits}",
        "- Relevance judgement: Not automatically inferred; manually review each result against the question.",
        "",
    ])
    OUTPUT_FILE.write_text("\n".join(lines), encoding="utf-8")
    print(f"Evaluation complete: {OUTPUT_FILE}")
    print(f"Executed {len(questions)} questions and recorded {total_hits} hits.")


if __name__ == "__main__":
    main()
