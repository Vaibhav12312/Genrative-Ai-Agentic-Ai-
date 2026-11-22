from app.repository import search_records


def search_epfo_knowledge(query: str) -> dict:
    """Agent tool: search the local EPFO knowledge base."""
    results = search_records(query, limit=5)
    return {
        "tool": "search_epfo_knowledge",
        "query": query,
        "results": results,
        "count": len(results),
    }


class EPFOAgent:
    """Small tool-using agent; tool results are passed to the configured LLM."""

    def __init__(self, llm):
        self.llm = llm

    def answer(self, question: str) -> tuple[str, list[int]]:
        tool_result = search_epfo_knowledge(question)
        records = tool_result["results"]
        context = "\n".join(
            f"[{r['id']}] {r['title']}: {r['content']}" for r in records
        )
        answer = self.llm.generate(question, context)
        return answer, [r["id"] for r in records]
