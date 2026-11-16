import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest
from fastapi.testclient import TestClient
from app.rag import EpfosathiRAG, ABSTENTION
from app.main import app

client = TestClient(app)


def test_q6_forced_abstention_exact_text():
    result = EpfosathiRAG().answer(
        "What is my personal EPF account balance right now?", "Q6"
    )
    assert result["answer"] == "I don't know"
    assert result["citations"] == []


def test_unknown_question_abstains():
    result = EpfosathiRAG().answer("What is the weather on Mars?")
    assert result["answer"] == ABSTENTION
    assert result["citations"] == []


def test_answer_has_citations():
    result = EpfosathiRAG().answer("What does UAN stand for?")
    assert "Universal Account Number" in result["answer"]
    assert result["citations"]
    assert result["citations"][0]["url"].startswith("https://")


def test_retrieve_top_k_limit():
    rag = EpfosathiRAG(top_k=2)
    assert len(rag.retrieve("UAN member passbook")) <= 2


def test_empty_question_rejected_by_engine():
    with pytest.raises(ValueError):
        EpfosathiRAG().answer("   ")


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ask_endpoint():
    response = client.post("/ask", json={"question": "What does UAN stand for?"})
    assert response.status_code == 200
    payload = response.json()
    assert "Universal Account Number" in payload["answer"]
    assert len(payload["citations"]) > 0


def test_ask_q6_endpoint():
    response = client.post("/ask", json={
        "question": "What is my personal EPF balance?",
        "question_id": "Q6"
    })
    assert response.status_code == 200
    assert response.json()["answer"] == "I don't know"
    assert response.json()["citations"] == []


def test_blank_question_validation():
    response = client.post("/ask", json={"question": "   "})
    assert response.status_code == 422


def test_missing_question_validation():
    response = client.post("/ask", json={})
    assert response.status_code == 422


def test_personal_balance_question_abstains_without_eval_id():
    result = EpfosathiRAG().answer("What is my personal EPF account balance right now?")
    assert result["answer"] == "I don't know"
    assert result["citations"] == []


def test_answer_returns_retrieved_chunks_and_matching_citations():
    result = EpfosathiRAG().answer("What does UAN stand for?")
    assert result["retrieved_chunks"]
    cited_ids = {citation["id"] for citation in result["citations"]}
    retrieved_ids = {chunk["source"]["id"] for chunk in result["retrieved_chunks"]}
    assert cited_ids
    assert cited_ids.issubset(retrieved_ids)


def test_q6_endpoint_returns_exact_abstention_without_evidence():
    response = client.post("/ask", json={
        "question": "What is my personal EPF account balance right now?",
        "question_id": "Q6",
    })
    assert response.status_code == 200
    payload = response.json()
    assert payload["answer"] == "I don't know"
    assert payload["citations"] == []
    assert payload["retrieved_chunks"] == []
