import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ui"))
from api_client import normalize_response, save_feedback, call_backend


def test_normalize_common_answer_and_citations():
    answer, citations = normalize_response({"answer": "PF answer", "citations": [{"title": "EPFO", "url": "https://epfindia.gov.in"}]})
    assert answer == "PF answer"
    assert citations == [{"label": "EPFO", "url": "https://epfindia.gov.in"}]


def test_normalize_string_response():
    assert normalize_response(" plain text ") == ("plain text", [])


def test_normalize_sources_as_strings_and_nested_data():
    answer, citations = normalize_response({"data": {"response": "hello", "sources": ["Circular 1"]}})
    assert answer == "hello" and citations[0]["label"] == "Circular 1"


def test_unknown_response_is_not_silently_empty():
    assert "no recognised answer" in normalize_response({"ok": True})[0]


def test_feedback_persists_and_rejects_invalid_vote(tmp_path):
    db = tmp_path / "feedback.sqlite3"
    save_feedback(db, "question", "answer", "up")
    import sqlite3
    with sqlite3.connect(db) as conn:
        row = conn.execute("SELECT question, answer, vote FROM feedback").fetchone()
    assert row == ("question", "answer", "up")
    try: save_feedback(db, "q", "a", "maybe")
    except ValueError: pass
    else: raise AssertionError("Expected invalid vote to fail")


def test_call_backend_builds_route_payload_and_auth(monkeypatch):
    import api_client
    class Response:
        def raise_for_status(self): pass
        def json(self): return {"answer": "ok", "citations": []}
    seen = {}
    def fake_post(url, **kwargs):
        seen.update(url=url, **kwargs); return Response()
    monkeypatch.setattr(api_client.requests, "post", fake_post)
    assert call_backend("http://localhost:8000/", "agent", "hello", [], "secret")[0] == "ok"
    assert seen["url"] == "http://localhost:8000/agent"
    assert seen["headers"]["Authorization"] == "Bearer secret"
    assert seen["json"]["question"] == "hello"


def test_invalid_endpoint_rejected():
    try: call_backend("http://localhost", "bad", "q", [])
    except ValueError: pass
    else: raise AssertionError("Expected invalid endpoint to fail")
