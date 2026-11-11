
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_records_default_limit():
    response = client.get("/records")

    assert response.status_code == 200
    assert response.json()["total"] == 20
    assert response.json()["returned"] == 10
    assert len(response.json()["records"]) == 10


def test_records_custom_limit():
    response = client.get("/records?limit=5")

    assert response.status_code == 200
    assert response.json()["returned"] == 5
    assert len(response.json()["records"]) == 5


def test_records_invalid_limit():
    response = client.get("/records?limit=0")

    assert response.status_code == 422


def test_record_by_id():
    response = client.get("/records/1")

    assert response.status_code == 200
    assert response.json()["faq_number"] == "1"


def test_record_missing_returns_404():
    response = client.get("/records/999")

    assert response.status_code == 404


def test_search():
    response = client.get("/search", params={"q": "PF withdrawal"})

    assert response.status_code == 200
    assert response.json()["query"] == "PF withdrawal"
    assert "results" in response.json()
    assert "total_results" in response.json()


def test_search_empty_query():
    response = client.get("/search", params={"q": ""})

    assert response.status_code == 422


def test_post_question():
    response = client.post(
        "/questions",
        json={"question": "How can I withdraw my PF?"}
    )

    assert response.status_code == 200
    assert response.json()["question"] == "How can I withdraw my PF?"
    assert "results" in response.json()
    assert "message" in response.json()


def test_post_question_too_short():
    response = client.post(
        "/questions",
        json={"question": "a"}
    )

    assert response.status_code == 422
