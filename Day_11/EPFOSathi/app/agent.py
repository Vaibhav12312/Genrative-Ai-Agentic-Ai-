"""Small tool-using assistant; model integration is injected for testability."""
from __future__ import annotations
from typing import Protocol, Any
from .records import RecordStore

class LLM(Protocol):
    def generate(self, question: str, context: list[dict[str, Any]]) -> str: ...

class KnowledgeTool:
    name = "search_epf_records"
    description = "Search the EPFOSathi knowledge records for relevant EPF/EPFO guidance."

    def __init__(self, store: RecordStore):
        self.store = store

    def run(self, query: str) -> list[dict[str, Any]]:
        return self.store.search(query)

class GroundedFallbackLLM:
    """Safe local response provider used when no external LLM is configured."""
    def generate(self, question: str, context: list[dict[str, Any]]) -> str:
        if not context:
            return "I could not find a matching item in the EPFOSathi knowledge base. Please verify the latest process on the official EPFO website."
        return " ".join(item["content"] for item in context[:3]) + " Please verify account-specific details on the official EPFO portal."

class EPFAgent:
    def __init__(self, store: RecordStore, llm: LLM | None = None):
        self.tool = KnowledgeTool(store)
        self.llm = llm or GroundedFallbackLLM()

    def ask(self, question: str) -> dict[str, Any]:
        records = self.tool.run(question)
        answer = self.llm.generate(question, records)
        return {"answer": answer, "sources": [{"id": r["id"], "title": r["title"]} for r in records], "tool": self.tool.name}
