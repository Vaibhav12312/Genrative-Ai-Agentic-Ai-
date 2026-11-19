from app.main import agent as default_agent

def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_records_endpoint(client):
    response = client.get("/api/records")
    assert response.status_code == 200
    assert response.json()["count"] >= 6

def test_search_endpoint(client):
    response = client.get("/api/search", params={"q": "UAN"})
    assert response.status_code == 200
    assert response.json()["count"] >= 1


def test_record_detail_endpoint(client):
    response = client.get("/api/records/UAN-001")
    assert response.status_code == 200
    assert response.json()["id"] == "UAN-001"


def test_search_requires_query(client):
    response = client.get("/api/search")
    assert response.status_code == 422

def test_record_not_found_endpoint(client):
    assert client.get("/api/records/missing").status_code == 404

def test_ask_endpoint_with_fake_llm(client, monkeypatch):
    class FakeLLM:
        def generate(self, question, context):
            assert question == "What is UAN?"
            assert context
            return "Fake grounded answer"
    from app import main
    monkeypatch.setattr(main, "agent", main.EPFAgent(main.store, FakeLLM()))
    response = client.post("/ask", json={"question": "What is UAN?"})
    assert response.status_code == 200
    assert response.json()["answer"] == "Fake grounded answer"
    assert response.json()["tool"] == "search_epf_records"
    monkeypatch.setattr(main, "agent", default_agent)

def test_ask_rejects_too_short_question(client):
    assert client.post("/ask", json={"question": "?"}).status_code == 422

def test_home_serves_ui(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "EPFOSathi" in response.text
