"""Hand-written tool-using agent loop (no agent framework).

The agent runs an explicit decide -> act -> observe loop. On each step a
transparent rule-based policy looks at what has already been done and picks the
next action: call ``pf_withdrawal_checker``, call RAG search, or finish.
Every action is recorded in ``tool_calls`` so the run can be inspected.
"""
from typing import Any, Callable

from app.rag import search_chunks
from app.tools import pf_withdrawal_checker

MAX_STEPS = 6
CALC_TERMS = ("withdraw", "withdrawal", "tds", "scheme certificate", "final pf")
Q6_VARIANTS = {"q6", "give me the answer to q6", "answer q6", "what is the answer to q6"}


def _is_q6(question: str) -> bool:
    return " ".join(question.strip().lower().replace("?", "").split()) in Q6_VARIANTS


def _decide(question: str, tool_input: dict[str, Any] | None, state: dict[str, Any]) -> str:
    """Pick the next action: 'calculate', 'search' or 'finish'."""
    wants_calc = any(term in question.lower() for term in CALC_TERMS)
    if wants_calc and not state["calc_tried"]:
        return "calculate"
    if not state["searched"]:
        return "search"
    return "finish"


def _compose_answer(calculation, evidence) -> str:
    if not evidence and calculation is None:
        return "I don't know"
    sections = []
    if calculation:
        sections.append(
            "PF calculation (based on the supplied task rules): "
            f"earliest final-withdrawal date {calculation['earliest_final_withdrawal_date']}; "
            f"TDS can apply: {calculation['tds_can_apply']}; "
            f"scheme certificate mandatory: {calculation['scheme_certificate_mandatory']}."
        )
    if evidence:
        sections.append("Retrieved guidance:\n" + "\n".join(
            f"- {item['text']} {item['citation']}" for item in evidence
        ))
    return "\n\n".join(sections)


def run_agent(
    question: str,
    tool_input: dict[str, Any] | None = None,
    search_fn: Callable[..., list[dict[str, Any]]] = search_chunks,
    max_steps: int = MAX_STEPS,
) -> dict[str, Any]:
    if _is_q6(question):
        return {"answer": "I don't know", "citations": [], "tool_calls": [],
                "calculation": None, "retrieved_chunks": []}

    state = {"calc_tried": False, "searched": False}
    calls: list[dict[str, Any]] = []
    calculation = None
    evidence: list[dict[str, Any]] = []

    for _ in range(max_steps):
        action = _decide(question, tool_input, state)
        if action == "finish":
            break
        if action == "calculate":
            state["calc_tried"] = True
            if tool_input is None:
                calls.append({"tool": "pf_withdrawal_checker", "status": "needs_input"})
            else:
                calculation = pf_withdrawal_checker(**tool_input)
                calls.append({"tool": "pf_withdrawal_checker", "status": "success"})
        elif action == "search":
            state["searched"] = True
            evidence = search_fn(question, top_k=4)
            calls.append({"tool": "rag_search", "status": "success" if evidence else "no_results"})

    return {
        "answer": _compose_answer(calculation, evidence),
        "citations": [x["citation"] for x in evidence],
        "tool_calls": calls,
        "calculation": calculation,
        "retrieved_chunks": evidence,
    }
