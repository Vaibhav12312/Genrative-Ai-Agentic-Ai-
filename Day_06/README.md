# EPFOSathi

A small FastAPI service that answers questions about **EPFO / Provident Fund** (UAN, KYC, PF balance, claims, transfers, EPS pension) using an LLM (**Groq** or **Gemini**).

> EPFOSathi gives general information only. It is not legal, tax or investment advice, and it is not an official EPFO service. Always confirm on the official EPFO member portal / epfindia.gov.in.

## What is implemented

### S1 - Provider wrapper + `/chat`
- `app/llm.py` - provider wrapper. One function `generate(system_prompt, user_prompt)` that calls **Groq** or **Gemini** depending on `LLM_PROVIDER` (plus an offline `mock` provider for demos/tests).
- `POST /chat` in `app/main.py` - sends the **EPFOSathi system prompt** with the user's question to the LLM.
- Secrets: `.env` is **git-ignored and not committed**; `.env.example` **is committed** with placeholder values.

### S2 - Prompts folder + structured JSON + prompt comparison
- `prompts/` - `system.md` (EPFOSathi persona, scope, safety rules, JSON format) and **two task prompts**: `task_v1.md` (basic) and `task_v2.md` (structured).
- `/chat` always returns JSON: `{"answer", "confidence", "follow_up"}` (validated with Pydantic, confidence clamped to 0-1, safe fallback if the model returns bad JSON).
- `eval/prompt_compare.md` - compares prompt v1 vs v2 on **10 questions** (`eval/questions.json`). `eval/run_eval.py` runs both versions and writes the results into that file. `eval/manual_scorecard.csv` provides a 20-row reviewer scorecard (10 questions x 2 versions) for the five 0-2 quality criteria.

## Project structure

```
epfo-sathi/
├── app/
│   ├── main.py        # FastAPI app: GET /health, POST /chat
│   ├── llm.py         # Groq / Gemini wrapper (+ mock)
│   ├── chat.py        # build prompt -> call LLM -> parse & validate JSON
│   ├── prompts.py     # loads files from prompts/
│   ├── schemas.py     # request/response models
│   └── config.py      # env-based settings
├── prompts/
│   ├── system.md      # EPFOSathi system prompt
│   ├── task_v1.md     # task prompt version 1 (basic)
│   └── task_v2.md     # task prompt version 2 (structured)
├── scripts/
│   └── check_submission.py  # verifies required files and unfinished evaluation placeholders
├── eval/
│   ├── questions.json     # the 10 test questions
│   ├── run_eval.py        # runs v1 vs v2 and fills the results
│   └── prompt_compare.md  # comparison write-up
├── tests/test_chat.py # unit tests (no API key needed)
├── .env.example       # committed template
├── .gitignore         # ignores .env
├── requirements.txt
└── README.md
```

## Setup

Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env               # Windows: copy .env.example .env
# edit .env: set LLM_PROVIDER and the matching API key
```

Get a free key: Groq -> https://console.groq.com/keys, Gemini -> https://aistudio.google.com/app/apikey.

| Variable | Meaning | Default |
|---|---|---|
| `LLM_PROVIDER` | `groq`, `gemini` or `mock` | `groq` |
| `GROQ_API_KEY` / `GROQ_MODEL` | Groq key / model | `llama-3.3-70b-versatile` |
| `GEMINI_API_KEY` / `GEMINI_MODEL` | Gemini key / model | `gemini-2.5-flash` |
| `LLM_TEMPERATURE` | sampling temperature | `0.2` |
| `LLM_MAX_TOKENS` | max output tokens | `700` |
| `LLM_TIMEOUT_SECONDS` | HTTP timeout | `30` |

Model names change over time - if a provider returns a "model not found" error, update the model in `.env`.

## Run

```bash
uvicorn app.main:app --reload
```
Interactive docs: http://127.0.0.1:8000/docs

## API

### `POST /chat`

Request:
```json
{ "message": "How do I activate my UAN?", "prompt_version": "v2" }
```
`prompt_version` is optional: `"v1"` or `"v2"` (default `"v2"`).

Response (always this shape):
```json
{
  "answer": "...",
  "confidence": 0.85,
  "follow_up": "Is your KYC already complete?"
}
```

Example:
```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the difference between EPF and EPS?"}'
```

Errors: `422` invalid input, `502` provider problem (missing key, upstream HTTP error).

### `GET /health`
Returns `{"status": "ok", "provider": "..."}`.

## Tests

```bash
pytest
```
Tests mock the LLM, so no API key or internet is needed.

## Prompt comparison (S2)

```bash
python -m eval.run_eval
```
This calls the configured provider for all 10 questions x 2 prompt versions (20 calls), then writes metrics and every answer into `eval/prompt_compare.md`. Read the outputs, complete `eval/manual_scorecard.csv`, then update the hand-scoring table and conclusion at the bottom of that file.

## Submission check

```bash
python -m scripts.check_submission
```
This checks the required project files, the Q6 personal-data boundary question, and the question-by-question prompt comparison. Live provider results are optional because they require an internet connection and a real API key; the report clearly distinguishes prompt-design analysis from measured model results.

## Evaluation status

The repository includes 10 fixed questions, a question-by-question comparison, and separate companion reports at `eval/reports/prompt_v1_report.md` and `eval/reports/prompt_v2_report.md`. These companion reports are prompt-design previews, not fabricated live scores. The repository includes 10 fixed questions and a question-by-question comparison of prompt v1 and v2. The checked-in report records that the attempted live Gemini evaluation was blocked by DNS/network access, so it does not invent model outputs or scores. To produce measured results, configure a real provider key and run:

```bash
python -m eval.run_eval
```

The script writes `eval/results.json` locally (ignored by Git) and updates the results section in `eval/prompt_compare.md`. Review all 20 outputs, complete `eval/manual_scorecard.csv`, and update the hand-scoring table before claiming a measured winner.

## Design notes
- **Prompts live in files**, not code, so they can be edited and versioned without touching Python.
- **The JSON contract is in the system prompt** (shared by both versions) so the comparison measures only the task-prompt difference. Both providers are additionally asked for JSON mode.
- **Robust parsing:** code fences are stripped, confidence is clamped, and unparseable output falls back to `confidence: 0.0` instead of crashing.
- **Privacy:** the system prompt forbids asking for OTP, password, Aadhaar, bank details or UAN.
- **No fabricated facts:** time-sensitive items (interest rate, limits) are redirected to official sources.
