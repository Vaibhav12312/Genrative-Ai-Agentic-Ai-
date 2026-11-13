# EPFOSathi

A small FastAPI service that answers common EPFO / Provident Fund questions from a checked FAQ
file, and honestly says "I don't have this" when the data can't answer.

## Project structure
```
epfosathi/
├── app/
│   ├── main.py            # FastAPI app: /health, /faq, /ask
│   └── data/
│       ├── faq.json               # 6 short curated answers (keyword matched)
│       ├── epfo_faq_records.py    # 20 original EPFO FAQ records (with source_url)
│       └── __init__.py
├── docs/
│   ├── how_llms_work.md   # LLM explanation + diagram
│   ├── questions.md       # 10 real user questions (Q6 unanswerable)
│   ├── checkpoint-1.md    # run steps + function explanation
│   ├── run_output.txt     # captured output of the running app
│   └── images/            # llm_flow.png + docs-page.png (/docs screenshot)
├── tests/test_main.py
├── requirements.txt
└── README.md
```

## Setup and run
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```
- Interactive docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## Endpoints
| Method | Path | Purpose |
|--------|------|---------|
| GET | `/health` | service status |
| GET | `/faq` | list known questions (6 curated + 20 original EPFO FAQs) |
| POST | `/ask` | body `{"question": "..."}`, returns answer or fallback |

Example:
```bash
curl -X POST http://127.0.0.1:8000/ask -H "Content-Type: application/json" \
  -d '{"question":"How do I check my PF balance?"}'
```

## How answers are found
1. `find_best_answer` checks the 6 curated entries by keyword.
2. If nothing matches, `find_original_faq` looks through the 20 original EPFO FAQ records
   (needs at least 2 meaningful words in common) and returns the answer with its `source_url`.
3. If both miss, the API says it does not have the answer (this is what happens for Q6).

## Tests
```bash
pytest
```

## Task checklist
- [x] `docs/how_llms_work.md` in my own words with 1 diagram
- [x] 10 real user questions in `docs/questions.md` (Q6 not answerable from data)
- [x] Checkpoint 1: FastAPI runs, `/docs` works, one function explained (`docs/checkpoint-1.md`)
- [x] Git tag `checkpoint-1`

## Limitations
Keyword / word-overlap matching only; the data is general and not a substitute for official EPFO information
(epfindia.gov.in). It has no access to any member's personal account.
