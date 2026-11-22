def test_agent_search_tool(client):
    client.post("/records", json={
        "title": "UAN activation",
        "content": "Activate UAN using the member portal.",
        "category": "account",
    })
    from app.agent import search_epfo_knowledge
    result = search_epfo_knowledge("UAN")
    assert result["tool"] == "search_epfo_knowledge"
    assert result["count"] == 1
    assert result["results"][0]["title"] == "UAN activation"


def test_agent_returns_source_ids(client):
    client.post("/records", json={
        "title": "Claim status",
        "content": "Track claim status online.",
        "category": "claims",
    })
    from app.agent import EPFOAgent
    class FakeLLM:
        def generate(self, question, context):
            return "Claim status guidance."
    answer, sources = EPFOAgent(FakeLLM()).answer("claim status")
    assert answer == "Claim status guidance."
    assert len(sources) == 1
