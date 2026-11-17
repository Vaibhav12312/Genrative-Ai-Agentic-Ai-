from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import Command

from app.graph import build_graph

INPUT = {"join_date": "2018-01-01", "exit_date": "2024-06-15", "age": 35, "resignation": True}


def _cfg(thread):
    return {"configurable": {"thread_id": thread}}


def test_graph_pauses_at_single_approval_step():
    g = build_graph(MemorySaver())
    g.invoke({"question": "What is UAN?", "tool_input": None}, config=_cfg("t1"))
    assert g.get_state(_cfg("t1")).next == ("approval",)


def test_graph_resume_approved_returns_cited_answer_and_calculation():
    g = build_graph(MemorySaver())
    g.invoke({"question": "When can I withdraw PF after resignation?", "tool_input": INPUT},
             config=_cfg("t2"))
    result = g.invoke(Command(resume={"approved": True}), config=_cfg("t2"))
    assert result["calculation"]["earliest_final_withdrawal_date"] == "2024-08-15"
    assert result["citations"]
    assert g.get_state(_cfg("t2")).next == ()


def test_graph_resume_declined():
    g = build_graph(MemorySaver())
    g.invoke({"question": "What is UAN?", "tool_input": None}, config=_cfg("t3"))
    result = g.invoke(Command(resume={"approved": False}), config=_cfg("t3"))
    assert result["answer"] == "Request not approved."
    assert result["citations"] == []


def test_graph_q6_abstains_after_approval():
    g = build_graph(MemorySaver())
    g.invoke({"question": "Give me the answer to Q6", "tool_input": None},
             config=_cfg("t-q6"))
    result = g.invoke(Command(resume={"approved": True}), config=_cfg("t-q6"))
    assert result["answer"] == "I don't know"
    assert result["citations"] == []


def test_graph_memory_is_scoped_per_thread():
    g = build_graph(MemorySaver())
    g.invoke({"question": "What is UAN?", "tool_input": None}, config=_cfg("a"))
    g.invoke({"question": "How do I submit an online EPF claim?", "tool_input": None}, config=_cfg("b"))
    assert g.get_state(_cfg("a")).values["question"] == "What is UAN?"
    assert g.get_state(_cfg("b")).values["question"] == "How do I submit an online EPF claim?"
