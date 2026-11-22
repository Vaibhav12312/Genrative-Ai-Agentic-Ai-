def add_sample(
    client,
    title="EPF passbook",
    content="Members can view passbook online.",
    category="passbook",
):
    return client.post(
        "/records",
        json={"title": title, "content": content, "category": category},
    )


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "EPFOSathi"}


def test_create_record(client):
    response = add_sample(client)
    assert response.status_code == 201
    assert response.json()["title"] == "EPF passbook"


def test_list_records(client):
    add_sample(client)
    response = client.get("/records")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_search_title(client):
    add_sample(client)
    response = client.get("/search", params={"q": "passbook"})
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_search_content(client):
    add_sample(client)
    assert len(client.get("/search", params={"q": "online"}).json()) == 1


def test_search_no_match(client):
    add_sample(client)
    assert client.get("/search", params={"q": "unmatched"}).json() == []


def test_pagination(client):
    add_sample(client, "One", "First")
    add_sample(client, "Two", "Second")
    response = client.get("/records", params={"limit": 1, "offset": 0})
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_record_validation(client):
    response = client.post("/records", json={"title": "", "content": "x"})
    assert response.status_code == 422


def test_search_validation(client):
    assert client.get("/search", params={"q": ""}).status_code == 422


def test_ask_with_fake_llm(client, monkeypatch):
    from app import main
    class FakeLLM:
        def generate(self, question, context):
            assert "passbook" in context.lower()
            return "Fake answer for testing."
    add_sample(client)
    monkeypatch.setattr(main, "get_llm", lambda: FakeLLM())
    response = client.post("/ask", json={"question": "How do I view passbook?"})
    assert response.status_code == 200
    assert response.json()["answer"] == "Fake answer for testing."
    assert len(response.json()["sources"]) == 1


def test_ask_without_matching_records(client, monkeypatch):
    from app import main
    class FakeLLM:
        def generate(self, question, context):
            assert context == ""
            return "No matching record."
    monkeypatch.setattr(main, "get_llm", lambda: FakeLLM())
    response = client.post("/ask", json={"question": "Unknown topic?"})
    assert response.status_code == 200
    assert response.json()["sources"] == []


def test_ask_validation(client):
    assert client.post("/ask", json={"question": "x"}).status_code == 422


def test_search_ignores_generic_epfo_terms(client):
    add_sample(
        client,
        title="EPF passbook",
        content="Members can view their EPF passbook online.",
        category="passbook",
    )

    response = client.get(
        "/search",
        params={"q": "What is my personal EPF account balance?"},
    )

    assert response.status_code == 200
    assert response.json() == []


def test_ask_does_not_send_irrelevant_records_to_llm(client, monkeypatch):
    from app import main

    class FakeLLM:
        def generate(self, question, context):
            assert context == ""
            return (
                "I cannot access your personal EPF account balance. "
                "Please check your EPF passbook through the official EPFO portal."
            )

    add_sample(client)

    monkeypatch.setattr(main, "get_llm", lambda: FakeLLM())

    response = client.post(
        "/ask",
        json={"question": "What is my personal EPF account balance?"},
    )

    assert response.status_code == 200
    assert response.json()["sources"] == []
    assert response.json()["source_details"] == []
    assert "cannot access" in response.json()["answer"].lower()

