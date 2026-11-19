def test_seed_records_exist(store):
    records = store.list_records()
    assert len(records) >= 6
    assert all({"id", "title", "category", "content"} <= item.keys() for item in records)

def test_get_existing_record(store):
    item = store.get_record("UAN-001")
    assert item is not None and item["category"] == "UAN"

def test_get_missing_record_returns_none(store):
    assert store.get_record("DOES-NOT-EXIST") is None

def test_search_is_case_insensitive(store):
    results = store.search("universal account number")
    assert any(item["id"] == "UAN-001" for item in results)

def test_search_empty_query_returns_empty(store):
    assert store.search("   ") == []

def test_search_limit_is_respected(store):
    assert len(store.search("EPF", limit=1)) <= 1
