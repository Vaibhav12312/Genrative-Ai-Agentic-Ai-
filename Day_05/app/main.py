"""EPFOSathi - a tiny FastAPI service that answers EPF questions from a small FAQ file.

Checkpoint 1 scope: the app runs, /docs works, and one function
(`find_best_answer`) is explained in docs/checkpoint-1.md.
"""
import json
import re
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

from app.data.epfo_faq_records import sample_records as EPFO_FAQ

DATA_FILE = Path(__file__).parent / "data" / "faq.json"
FALLBACK = (
    "I don't have this in my EPFO data. Please check epfindia.gov.in, "
    "call the EPFO helpline, or file a grievance on EPFiGMS."
)

app = FastAPI(
    title="EPFOSathi API",
    description="Simple EPF helper that answers from a small FAQ dataset.",
    version="0.1.0",
)


def load_faq() -> list[dict]:
    with open(DATA_FILE, encoding="utf-8") as f:
        return json.load(f)


FAQ = load_faq()  # short curated answers with keywords (checked first)

# Words that carry no meaning for matching the original EPFO FAQ questions.
STOPWORDS = {
    "a", "an", "the", "is", "are", "be", "can", "i", "my", "me", "do", "does",
    "how", "what", "when", "where", "why", "whether", "to", "of", "in", "on",
    "for", "and", "or", "if", "it", "he", "his", "she", "her", "any", "there",
    "that", "this", "with", "from", "by", "as", "at", "not", "no", "get", "will",
    "after", "even", "while", "also", "only", "long", "my", "your", "we", "you",
}


class AskRequest(BaseModel):
    question: str = Field(..., min_length=3, examples=["How do I activate my UAN?"])


class AskResponse(BaseModel):
    answered: bool
    matched_id: str | None
    answer: str
    source_url: str | None = None


def tokenize(text: str) -> set[str]:
    """Lowercase the text and split it into a set of words/numbers."""
    return set(re.findall(r"[a-z0-9%]+", text.lower()))


def find_best_answer(question: str) -> dict | None:
    """Score every FAQ entry by how many of its keywords appear in the
    question, and return the entry with the highest score.
    Returns None when nothing matches (so the API can say "I don't know"
    instead of making something up)."""
    q_text = question.lower()
    q_words = tokenize(question)
    best, best_score = None, 0
    for item in FAQ:
        score = 0
        for kw in item["keywords"]:
            # multi-word keywords are checked as phrases, single words as tokens
            if (" " in kw and kw in q_text) or kw in q_words:
                score += 1
        if score > best_score:
            best, best_score = item, score
    return best


def content_words(text: str) -> set[str]:
    """Meaningful words of a text: stop-words removed and a tiny stemmer
    applied so that 'withdraw'/'withdrawal' or 'resign'/'resignation' match."""
    words = set()
    for w in tokenize(text):
        if w in STOPWORDS:
            continue
        for suffix in ("ation", "ing", "ed", "al", "s"):
            if w.endswith(suffix) and len(w) - len(suffix) >= 4:
                w = w[: -len(suffix)]
                break
        words.add(w)
    return words


def find_original_faq(question: str, min_overlap: int = 2) -> dict | None:
    """Second-chance lookup in the 20 original EPFO FAQ records.

    Counts the meaningful words the question shares with each record's
    question. At least `min_overlap` shared words are needed, otherwise
    None is returned (so we still say "I don't know" instead of guessing).
    """
    q_words = content_words(question)
    best, best_score = None, 0
    for rec in EPFO_FAQ:
        score = len(q_words & content_words(rec["question"]))
        if score > best_score:
            best, best_score = rec, score
    return best if best_score >= min_overlap else None


@app.get("/health")
def health():
    return {
        "status": "ok",
        "faq_entries": len(FAQ),
        "original_epfo_faq_records": len(EPFO_FAQ),
    }


@app.get("/faq")
def list_faq():
    curated = [{"id": i["id"], "question": i["question"]} for i in FAQ]
    original = [
        {"id": f"epfo-faq-{r['faq_number']}", "question": r["question"]}
        for r in EPFO_FAQ
    ]
    return curated + original


@app.post("/ask", response_model=AskResponse)
def ask(req: AskRequest):
    match = find_best_answer(req.question)
    if match is not None:
        return AskResponse(answered=True, matched_id=match["id"], answer=match["answer"])
    record = find_original_faq(req.question)
    if record is not None:
        return AskResponse(
            answered=True,
            matched_id=f"epfo-faq-{record['faq_number']}",
            answer=record["answer"],
            source_url=record["source_url"],
        )
    return AskResponse(answered=False, matched_id=None, answer=FALLBACK)
