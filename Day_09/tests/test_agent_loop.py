from app.agent_loop import run_agent

INPUT = {"join_date": "2018-01-01", "exit_date": "2024-06-15", "age": 35}


def test_manual_agent_calls_calculator_and_rag():
    result = run_agent("Calculate PF withdrawal and TDS", INPUT)
    assert result["calculation"]["earliest_final_withdrawal_date"] == "2024-08-15"
    tools = [call["tool"] for call in result["tool_calls"]]
    assert tools == ["pf_withdrawal_checker", "rag_search"]
    assert all(call["status"] == "success" for call in result["tool_calls"])


def test_agent_skips_calculator_for_plain_question():
    result = run_agent("What is UAN?")
    assert [c["tool"] for c in result["tool_calls"]] == ["rag_search"]
    assert result["calculation"] is None
    assert "[EPF-001]" in result["citations"]


def test_agent_reports_needs_input_without_tool_input():
    result = run_agent("When can I withdraw PF?")
    assert result["tool_calls"][0] == {"tool": "pf_withdrawal_checker", "status": "needs_input"}
    assert result["calculation"] is None


def test_agent_abstains_when_nothing_found():
    result = run_agent("Tell me my private bank balance", search_fn=lambda *a, **k: [])
    assert result["answer"] == "I don't know"


def test_agent_q6_abstains_without_tools():
    result = run_agent("Give me the answer to Q6")
    assert result["answer"] == "I don't know"
    assert result["tool_calls"] == [] and result["citations"] == []


def test_agent_loop_is_bounded():
    result = run_agent("What is UAN?", max_steps=1)
    assert len(result["tool_calls"]) <= 1
