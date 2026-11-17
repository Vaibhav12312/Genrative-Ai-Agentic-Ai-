
# EPFOSathi V2 — RAG + Tool Agent + LangGraph

A small, locally runnable EPF guidance assistant implementing the requested S1 and S2 work:
- RAG retrieval with source citations and abstention.
- `pf_withdrawal_checker` deterministic calculator in `app/tools.py`.
- Hand-written tool-using agent loop in `app/agent_loop.py` (explicit decide → act → observe loop, bounded by `max_steps`, calling RAG search and the calculator).
- LangGraph implementation with thread-scoped memory and one real interrupt/resume approval gate in `app/graph.py`.
- FastAPI endpoints: `POST /ask`, `POST /agent`, plus `POST /agent/loop`.

> **Important:** The PF calculator encodes the simplified rules explicitly requested for this assignment. It is not a legal, tax, or EPFO eligibility determination. Real claims may depend on current EPFO rules, exceptions, member details, and official records. Verify before acting.

## Requirements

- Python 3.10+
- pip

## Setup

```bash
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

## Run the API

```bash
uvicorn app.main:app --reload
```

Open:
- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

## API examples

### RAG — `POST /ask`

```json
{
  "question": "What is UAN?",
  "top_k": 4
}
```

Q6 abstention check:

```json
{"question": "Q6"}
```

Expected answer: exactly `I don't know`, with no citations.

### LangGraph agent — `POST /agent`

First call without approval:

```json
{
  "question": "When can I withdraw PF after resignation?",
  "thread_id": "member-session-001",
  "tool_input": {
    "join_date": "2018-01-01",
    "exit_date": "2024-06-15",
    "age": 35,
    "resignation": true
  }
}
```

Expected: `approval_required: true`. This is the single approval gate.

Repeat with the same `thread_id` and explicit approval:

```json
{
  "thread_id": "member-session-001",
  "approved": true
}
```

The graph returns retrieved evidence, citations, and (when provided) the calculator result.

### Hand-written agent loop — `POST /agent/loop`

Uses the manual loop rather than LangGraph:

```json
{
  "question": "Calculate PF withdrawal and TDS",
  "thread_id": "manual-001",
  "tool_input": {
    "join_date": "2018-01-01",
    "exit_date": "2024-06-15",
    "age": 35,
    "resignation": true
  }
}
```

## Calculator rules

`pf_withdrawal_checker(join_date, exit_date, age, resignation=True)` returns:
- completed service years;
- earliest final-withdrawal date: exit date plus two calendar months after resignation (month-end dates are clamped safely);
- `tds_can_apply`: true when completed service is under 5 years;
- `scheme_certificate_mandatory`: true when completed service is at least 10 years and age is under 58.

Dates must use `YYYY-MM-DD`. Invalid dates, exit-before-join, invalid age, and non-boolean resignation are rejected.

## Memory and approval design

`app/graph.py` compiles a LangGraph `StateGraph` with `MemorySaver`. The `thread_id` passed in the API config scopes checkpointed state to a conversation. The graph has three nodes in order: retrieval, calculation, and one approval node. The approval node uses LangGraph `interrupt()` to pause and checkpoint execution.
Call `POST /agent` first without the `approved` field. It returns
`approval_required: true`. Then call the same endpoint with the same `thread_id`
and `approved: true` (or false) to resume that exact pending run using
`Command(resume=...)`. A resume call without a matching pending run returns an error.

The included checkpointer is in-memory: state is retained while the process runs,
and is lost on restart. Use a durable LangGraph checkpointer for production. For production persistence, replace `MemorySaver` with a durable LangGraph checkpointer and configure its backing database.

## Tests and evaluation

Run all automated tests:

```bash
pytest -q
```

Run the two retrieval configurations against the exact 15-row evaluation set:

```bash
python eval/run_eval.py
```

The evaluation reports source-hit accuracy for:
- baseline: chunk size 450 / top-k 4;
- comparison: chunk size 700 / top-k 6.

`Q6` is checked as an exact abstention (`I don't know`) independently of retrieval.

## Project structure

```text
EPFOSathi_V2/
├── app/
│   ├── __init__.py
│   ├── agent_loop.py
│   ├── graph.py
│   ├── main.py
│   ├── rag.py
│   └── tools.py
├── data/
│   └── source_docs.json
├── eval/
│   ├── eval_set.json
│   └── run_eval.py
├── tests/
│   ├── test_agent_loop.py
│   ├── test_api.py
│   ├── test_graph.py
│   └── test_tools.py
├── .gitignore
├── README.md
└── requirements.txt
```

## Scope and known limitations

- Retrieval is deliberately transparent lexical overlap over the included compact evidence corpus; it does not call a paid embedding model or external API.
- `chunk_size` is exposed for the evaluation contract; the bundled corpus is already stored as concise chunks.
- This is a runnable assignment implementation, not a production EPFO service. Add official, versioned source documents and review legal/tax rules before deployment.


## V2 changes

- Approval is a genuine LangGraph interrupt/resume, not just a boolean branch.
- The same `thread_id` is required to resume the paused request.
- `/ask`, the manual agent, and LangGraph agent recognize the Q6 prompt variants and abstain exactly.
- Retrieval now removes common stopwords, boosts title matches, validates document fields,
  and applies the configured chunk-size limit.
- Tests cover approval pause/resume and Q6 wording in addition to calculator boundaries.

## Verification status

This build was syntax-compiled and its JSON files were validated when packaged.
The full pytest suite and LangGraph runtime integration still need to be run in an
environment where `requirements.txt` dependencies are installed. Do not interpret
syntax validation as a passing integration-test report.
