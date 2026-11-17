from app.chunking import chunk_documents


def test_chunking_preserves_source_title_page():
    docs = [{
        "text": "A" * 250,
        "title": "EPFO Claim FAQ",
        "source": "https://www.epfindia.gov.in/faq",
        "page": 7,
        "document_id": "faq-7",
    }]
    chunks = chunk_documents(docs, chunk_size=120, overlap=20)
    assert len(chunks) >= 2
    assert all(item["title"] == "EPFO Claim FAQ" for item in chunks)
    assert all(item["source"] == "https://www.epfindia.gov.in/faq" for item in chunks)
    assert all(item["page"] == 7 for item in chunks)
    assert chunks[0]["chunk_index"] == 0


def test_empty_document_is_skipped():
    assert chunk_documents([{"text": " ", "title": "Empty"}]) == []


def test_chunking_rejects_invalid_overlap():
    import pytest
    with pytest.raises(ValueError):
        chunk_documents([{"text": "A" * 200}], chunk_size=100, overlap=100)


def test_chunking_generates_stable_ids():
    doc = {"text": "A" * 250, "title": "Title", "source": "source.pdf", "page": 2}
    first = chunk_documents([doc], chunk_size=120, overlap=20)
    second = chunk_documents([doc], chunk_size=120, overlap=20)
    assert [x["id"] for x in first] == [x["id"] for x in second]


def test_json_loader_retains_title_source_and_page(tmp_path):
    import json
    from app.chunking import load_documents

    source = tmp_path / "faq.json"
    source.write_text(json.dumps([{
        "id": "faq-12", "question": "How to transfer PF?",
        "answer": "Use the member portal.", "source_url": "https://www.epfindia.gov.in/faq",
        "page": 12,
    }]), encoding="utf-8")
    docs = load_documents([source])
    assert len(docs) == 1
    assert docs[0]["title"] == "How to transfer PF?"
    assert docs[0]["source"] == "https://www.epfindia.gov.in/faq"
    assert docs[0]["page"] == 12



def test_bundled_epfo_faq_corpus_has_twenty_traceable_records():
    from pathlib import Path
    from app.chunking import load_documents

    corpus = Path(__file__).resolve().parents[1] / "data" / "documents" / "epfosathi_faqs.json"
    docs = load_documents([corpus])
    assert len(docs) == 20
    assert all(doc["title"] and doc["source"] for doc in docs)
    assert all(doc["page"] is None for doc in docs)
    assert any("transfer" in doc["title"].lower() for doc in docs)
