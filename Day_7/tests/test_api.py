from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)


def test_semantic_search_rejects_too_short_query():
    response = client.get("/search/semantic", params={"q": "hi"})
    assert response.status_code == 422


def test_semantic_search_requires_q():
    response = client.get("/search/semantic")
    assert response.status_code == 422


def test_semantic_search_returns_provenance(monkeypatch):
    monkeypatch.setattr(main, "semantic_search", lambda query, k=5: [{
        "id": "chunk-1", "text": "Claim guidance", "title": "EPFO FAQ",
        "source": "official-faq.pdf", "page": 3, "similarity": 0.91,
    }])
    response = client.get("/search/semantic", params={"q": "How do I claim PF?"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["count"] == 1
    assert payload["results"][0]["title"] == "EPFO FAQ"
    assert payload["results"][0]["source"] == "official-faq.pdf"
    assert payload["results"][0]["page"] == 3


def test_semantic_search_maps_empty_index_to_503(monkeypatch):
    def not_ready(query, k=5):
        raise RuntimeError("Chroma collection is empty")
    monkeypatch.setattr(main, "semantic_search", not_ready)
    response = client.get("/search/semantic", params={"q": "PF transfer"})
    assert response.status_code == 503
