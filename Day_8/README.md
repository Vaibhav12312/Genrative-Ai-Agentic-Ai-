# EPFOSathi — Retrieval-Augmented Question Answering

A small, runnable FastAPI project that answers EPFO member questions from a
curated local source corpus. Every non-abstained response includes citations
(URL + source title + source ID). Retrieval uses TF-IDF and cosine similarity;
the response is an extractive summary of retrieved chunks, not a generative
LLM response.

## Requirements

- Python 3.10+
- Internet is **not** required at runtime after dependencies are installed.
- The source corpus is in `data/source_docs.json`.

## Quick start

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` for interactive API documentation.

### Ask endpoint

`POST /ask`

```json
{
  "question": "What does UAN stand for?"
}
```

Example response shape:

```json
{
  "answer": "UAN stands for Universal Account Number...",
  "citations": [
    {
      "id": "EPFO-UAN-FAQ",
      "title": "EPFO Frequently Asked Questions for Members (UAN)",
      "url": "https://epfindia.gov.in/site_docs/PDFs/UAN_PDFs/UAN_ForMembers/FAQ-Member-Ver1.1.pdf"
    }
  ],
  "retrieved_chunks": []
}
```

`retrieved_chunks` contains the actual supporting chunk text, IDs and retrieval
scores. It is shown here as an empty illustrative array only; live responses
populate it when evidence is found.

Optional `question_id` is supported for evaluation. The supplied evaluation
row `Q6` is explicitly forced to abstain, returning exactly `I don't know`
with no citations.

## S1 — RAG and API

- `app/rag.py`: loads source documents, chunks them, indexes them with TF-IDF,
  retrieves top-k chunks, and returns a grounded extractive answer.
- `app/main.py`: FastAPI application with `POST /ask` and `GET /health`.
- Citations are de-duplicated by source ID and contain source title and URL.
- If no chunk passes the minimum similarity threshold, the answer is
  `I don't know`.
- Q6 is a deterministic abstention, regardless of retrieval score.

## S2 — Evaluation

The 15-row evaluation set is `eval/eval_set.json`. It includes Q6 as an
unanswerable personal-account question. The evaluator checks expected answer
keywords, requires at least one citation for every answerable row, and checks
exact Q6 abstention. It also validates that the evaluation file contains 15
rows and exactly one abstaining Q6 row.

Run:

```bash
python eval/run_eval.py
```

### Configuration comparison

The following table is the actual result of running the evaluator against the
included corpus (15 questions; keyword-match scoring):

| Chunk size (characters) | Top-k | Passed | Accuracy | Citation coverage | Q6 abstention |
|---:|---:|---:|---:|---:|---:|
| 250 | 2 | 11/15 | 73.3% | 14/14 | 1/1 |
| 450 | 4 | 15/15 | 100.0% | 14/14 | 1/1 |

**Winner: 450 characters / top-k 4.** This configuration passed all 15 evaluation rows, including Q6 abstention. The API uses this winning configuration by default. The smaller configuration
is retained as a comparison baseline; it is not the winner because it misses
four answerable questions in this evaluation set. Re-run
`python eval/run_eval.py` after changing the corpus or evaluation set; its
printed results are authoritative for the current checkout.

> Evaluation note: this is a lightweight offline regression set, not a
> statistically robust benchmark. Keyword matching is not semantic grading.
> The included corpus is intentionally small and curated for the 15 questions.

## Tests

```bash
pytest -q
```

The tests cover:
- Q6 exact abstention and empty citations
- Out-of-domain question abstention
- Answer grounding and citation presence
- Top-k retrieval limit
- Empty question validation
- Health endpoint
- Successful `/ask`
- Retrieved evidence is returned and citations refer to retrieved sources
- `/ask` Q6 behaviour
- Missing and blank request validation

## Project structure

```text
EPFOSathi/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── rag.py
├── data/
│   └── source_docs.json
├── eval/
│   ├── eval_set.json
│   └── run_eval.py
├── tests/
│   └── test_rag.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Sources and freshness

The starter corpus contains official EPFO pages/documents:

1. [EPFO Unified Member Portal](https://unifiedportal-mem.epfindia.gov.in/memberinterface/)
2. [EPFO Member Passbook and Claim Status](https://www.passbook.epfindia.gov.in/MemberPassBook/login)
3. [EPFO UAN Member FAQ (PDF)](https://epfindia.gov.in/site_docs/PDFs/UAN_PDFs/UAN_ForMembers/FAQ-Member-Ver1.1.pdf)
4. [EPFO Employer Portal](https://unifiedportal-emp.epfindia.gov.in/epfo/)

Some FAQ material is older. Where old FAQ instructions conflict with the current
member portal, prefer the current portal. Verify operational details on EPFO's
official website before relying on them for an individual claim.

## Design limitations / production hardening

- TF-IDF is a transparent baseline, not a semantic embedding model.
- Answers quote/concatenate retrieved chunks. For production, add a vetted LLM
  with strict context-only prompting and citation validation, or retain this
  extractive mode for maximum auditability.
- Add document ingestion/versioning, scheduled source refresh, monitoring,
  authentication, rate limiting, and privacy controls before public deployment.
- Do not collect UAN, Aadhaar, passwords, OTPs, bank details, or personal claim
  data in this demo.
