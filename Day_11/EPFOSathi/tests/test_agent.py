def test_agent_uses_knowledge_tool_and_returns_sources(agent):
    result = agent.ask("How do I check my PF claim status?")
    assert result["tool"] == "search_epf_records"
    assert isinstance(result["answer"], str) and result["answer"]
    assert result["sources"]

def test_agent_safe_fallback_when_no_records_match(agent):
    result = agent.ask("unrelated astronomy question")
    assert "could not find" in result["answer"].lower()
    assert result["sources"] == []

def test_agent_tool_is_callable(store):
    from app.agent import KnowledgeTool
    tool = KnowledgeTool(store)
    assert tool.name == "search_epf_records"
    assert tool.run("KYC")
