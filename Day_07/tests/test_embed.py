import pytest

from app import embed


class FakeVectors(list):
    def tolist(self):
        return list(self)


class FakeModel:
    def encode(self, texts, **kwargs):
        assert kwargs["normalize_embeddings"] is True
        return FakeVectors([[float(len(text)), 1.0] for text in texts])


def test_embed_texts_uses_model(monkeypatch):
    monkeypatch.setattr(embed, "get_model", lambda: FakeModel())
    assert embed.embed_texts(["abc", "hello"]) == [[3.0, 1.0], [5.0, 1.0]]


def test_embed_texts_empty_input():
    assert embed.embed_texts([]) == []


def test_embed_query_rejects_blank_query():
    with pytest.raises(ValueError):
        embed.embed_query("  ")
