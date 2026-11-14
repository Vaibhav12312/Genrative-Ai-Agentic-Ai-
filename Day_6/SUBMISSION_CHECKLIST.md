# S1 / S2 Submission Checklist

## S1 — Provider wrapper and API
- [x] `app/llm.py` provides a single `generate(system_prompt, user_prompt)` interface.
- [x] Groq provider uses the Groq chat-completions REST API.
- [x] Gemini provider uses the Gemini generate-content REST API.
- [x] Offline `mock` provider supports demos and tests without an API key.
- [x] `POST /chat` loads the EPFOSathi system prompt and returns the validated response model.
- [x] `.env` is excluded from Git; `.env.example` is included with placeholder values only.

## S2 — Prompt files and structured response
- [x] `prompts/system.md` defines EPFOSathi role, scope, privacy/safety boundaries and strict JSON output.
- [x] `prompts/task_v1.md` and `prompts/task_v2.md` provide two distinct task prompt versions.
- [x] `/chat` returns `answer`, `confidence`, and `follow_up`.
- [x] `eval/questions.json` contains 10 questions; Q6 deliberately asks for private passbook/contribution data unavailable to this app.
- [x] `eval/prompt_compare.md` compares v1 and v2 across all 10 questions and clearly distinguishes prompt-design analysis from measured live results.

## Verification performed for this packaged folder
- [x] `python -m pytest -q` — 18 tests passed.
- [x] `python -m scripts.check_submission` — all required submission checks passed.
- [x] FastAPI `/docs` and `/openapi.json` return HTTP 200.
- [x] Groq and Gemini request construction tested with mocked HTTP responses (no real credentials used).
- [x] No real `.env` file or API key is included.
- [ ] Live 20-call provider evaluation is pending a network-enabled environment and a valid Groq or Gemini API key. The report does not fabricate model outputs or scores.


