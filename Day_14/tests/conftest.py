import pytest
from fastapi.testclient import TestClient

from app import main
from app.database import init_db


@pytest.fixture()
def client(tmp_path, monkeypatch):
    monkeypatch.setattr("app.database.DB_PATH", tmp_path / "test.db")
    main.cache.clear()
    main.llm.calls = 0
    init_db()
    with TestClient(main.app) as test_client:
        yield test_client
