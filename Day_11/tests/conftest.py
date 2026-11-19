import pytest
from fastapi.testclient import TestClient
from app.agent import EPFAgent
from app.main import app
from app.records import RecordStore

@pytest.fixture
def store(tmp_path):
    return RecordStore(str(tmp_path / "test.db"))

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def agent(store):
    return EPFAgent(store)
