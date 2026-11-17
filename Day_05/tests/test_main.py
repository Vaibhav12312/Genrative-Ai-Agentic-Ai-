from fastapi.testclient import TestClient

from app.main import app, find_best_answer

client = TestClient(app)


def test_health():
    r = client.get("/health")
    assert r.status_code == 200 and r.json()["status"] == "ok"


def test_uan_question_is_answered():
    r = client.post("/ask", json={"question": "How do I activate my UAN?"})
    assert r.json()["answered"] is True
    assert r.json()["matched_id"] == "uan"


def test_unanswerable_question_falls_back():
    r = client.post("/ask", json={"question": "My claim is pending for 3 weeks, when will I get the money?"})
    assert r.json()["answered"] is False


def test_find_best_answer_none():
    assert find_best_answer("hello world") is None


def test_all_ten_questions_in_docs():
    expected = {
        "What is a UAN and how do I activate it?": "uan",
        "How much is deducted from my salary for PF and what does my employer pay?": "contribution",
        "How do I check my PF balance?": "passbook",
        "How do I transfer my PF when I change my job?": "transfer",
        "Why do I need to link Aadhaar and bank account with my UAN?": "kyc",
        "My claim was filed 3 weeks ago and is still pending. When will the money reach my account?": None,
        "Where can I file a complaint against EPFO?": "grievance",
        "How do I know whether my employer is actually depositing my PF every month?": "passbook",
        "Is my UAN the same when I change companies?": "uan",
        "Can I update my bank details if the old account is closed?": "kyc",
    }
    for q, fid in expected.items():
        m = find_best_answer(q)
        assert (m["id"] if m else None) == fid, q


def test_original_epfo_faq_records_loaded():
    from app.data.epfo_faq_records import sample_records

    assert len(sample_records) == 20
    assert all(r["source_url"].startswith("https://www.epfo.gov.in") for r in sample_records)
    assert client.get("/health").json()["original_epfo_faq_records"] == 20


def test_faq_endpoint_lists_curated_and_original():
    ids = [i["id"] for i in client.get("/faq").json()]
    assert "uan" in ids and "epfo-faq-1" in ids and "epfo-faq-20" in ids
    assert len(ids) == 6 + 20


def test_original_faq_answers_with_source():
    r = client.post("/ask", json={"question": "Is there an age limit to become an EPF member?"}).json()
    assert r["answered"] is True
    assert r["matched_id"] == "epfo-faq-14"
    assert r["source_url"] == "https://www.epfo.gov.in/faq-epfo/"


def test_q6_still_unanswerable_with_original_faqs():
    q = "My claim was filed 3 weeks ago and is still pending. When will the money reach my account?"
    r = client.post("/ask", json={"question": q}).json()
    assert r["answered"] is False and r["matched_id"] is None
