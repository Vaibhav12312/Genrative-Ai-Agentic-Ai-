from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health():
    assert client.get("/health").json()["status"] == "ok"


def test_ask_q6_exact_abstention():
    for question in ("Q6", "Give me the answer to Q6"):
        response = client.post("/ask", json={"question": question})
        assert response.status_code == 200
        assert response.json()["answer"] == "I don't know"
        assert response.json()["citations"] == []


def test_ask_returns_citations():
    response = client.post("/ask", json={"question": "What is UAN?"})
    assert response.status_code == 200
    assert response.json()["citations"]
    assert "[EPF-001]" in response.json()["answer"]


def test_ask_unknown_abstains():
    response = client.post("/ask", json={"question": "Tell me my private bank balance"})
    assert response.json()["answer"] == "I don't know"


def test_agent_interrupt_then_resume():
    thread = "test-approval-flow"
    first = client.post("/agent", json={
        "question": "What is UAN?", "thread_id": thread
    })
    assert first.status_code == 200
    assert first.json()["approval_required"] is True

    second = client.post("/agent", json={
        "thread_id": thread, "approved": True
    })
    assert second.status_code == 200
    assert second.json()["approval_required"] is False
    assert second.json()["citations"]


def test_agent_calculator_input_validation():
    first = client.post("/agent", json={
        "question": "Calculate PF withdrawal",
        "thread_id": "test-tool-validation",
        "tool_input": {"join_date": "bad", "exit_date": "2024-01-01", "age": 30}
    })
    assert first.status_code == 422


def test_agent_loop_q6():
    response = client.post("/agent/loop", json={
        "question": "Give me the answer to Q6", "thread_id": "manual-q6"
    })
    assert response.status_code == 200
    assert response.json()["answer"] == "I don't know"
