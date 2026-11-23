# EPFOSathi — Day 10 + Day 12 Integrated

[![CI](https://github.com/Vaibhav12312/Genrative-Ai-Agentic-Ai-/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/Vaibhav12312/Genrative-Ai-Agentic-Ai-/actions/workflows/ci.yml)

EPFOSathi is an informational assistant for general EPF/EPFO questions. This integrated project combines the Day 12 FastAPI/agent/LLM backend with the earlier browser interface and six-record EPFO knowledge set.

> **Safety note:** This is not an official EPFO service and does not access member accounts, submit claims, or verify live claim status. Do not enter UAN, Aadhaar, PAN, bank details, passwords, or OTPs. Confirm account-specific matters through official EPFO channels.

## Included features

- FastAPI application with `/docs` and `/health`.
- Day 12 record API: `POST /records`, `GET /records`, `GET /search`.
- Agent-backed `POST /ask` with source record IDs and source titles.
- Mock LLM by default; optional OpenAI-compatible adapter.
- Earlier browser UI at `/`, served from `app/static/index.html`.
- Backward-compatible UI routes: `GET /api/records`, `GET /api/records/{record_id}`, and `GET /api/search?q=...`.
- Six original knowledge records: UAN-001, KYC-001, CLAIM-001, PASSBOOK-001, TRANSFER-001, GRIEVANCE-001.
- Safe migration from the earlier SQLite schema with text primary keys to the current integer-key schema. Original IDs are retained in `legacy_id`.
- Idempotent seed script: safe to run more than once.
- Docker and Render configuration, plus GitHub Actions CI.

## Run locally (Windows PowerShell)

Extract the ZIP. Open PowerShell in the extracted `EPFOSathi_S1_S2_CI_Deploy_Ready` folder — the folder that directly contains `pyproject.toml`, `app`, `scripts`, and `tests`.

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m scripts.seed
uvicorn app.main:app --reload
```

Open:
- Browser app: http://127.0.0.1:8000/
- API docs: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

For macOS/Linux, activate with `source .venv/bin/activate`.

## Seed data

Run `python -m scripts.seed` from the project root. The script loads `data/seed.json` and inserts records by their stable `legacy_id`; rerunning it does not duplicate the six starter records.

If you have an older Day 10 database using text IDs, back it up first and configure `DATABASE_PATH` to point to a copy of that database. On startup, `init_db()` detects the old schema, migrates the records into the current schema, preserves their former IDs in `legacy_id`, and replaces the old table with the new schema. Do not point the app at your only copy of an important database without taking a backup.

## API quick reference

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health |
| POST | `/records` | Create a knowledge record |
| GET | `/records?limit=100&offset=0` | List records |
| GET | `/search?q=UAN` | Search records |
| POST | `/ask` | Ask the agent; returns answer and source IDs |
| GET | `/api/records` | Legacy UI list response |
| GET | `/api/records/{record_id}` | Legacy detail route; accepts integer or legacy text ID |
| GET | `/api/search?q=UAN` | Legacy UI search response |

Example ask request:

```json
{"question": "How can I check my PF claim status?"}
```

The response includes `answer`, `sources` (integer database IDs), and `source_details` (titles and preserved legacy IDs). The browser UI uses source titles where available.

## LLM configuration

The default `LLM_PROVIDER=mock` uses a deterministic local adapter and does not require an API key.

To enable the optional OpenAI adapter, install the extra and set environment variables:

```powershell
pip install -e ".[openai]"
$env:LLM_PROVIDER="openai"
$env:OPENAI_API_KEY="your-key"
```

Never commit `.env` or API keys. `.env.example` is provided as a template.

## Tests and lint

```powershell
pytest -q
ruff check .
```

The test suite covers the Day 12 record API, agent and LLM injection, safe no-match behavior, legacy frontend routes, the six original stable IDs, and migration from the earlier text-ID database schema.

## Docker

Build and run directly (no Compose file is required):

```powershell
docker build -t epfosathi .
docker run --rm -p 8000:8000 epfosathi
```

The container seeds the six starter records before starting Uvicorn. Open http://localhost:8000. For persistent local data, mount a host directory at `/app/data`.

## Deployment (Render)

A Render Blueprint is included in `render.yaml`. To deploy:

1. Push this project to the GitHub repository.
2. In Render, choose **New → Blueprint**, connect `Vaibhav12312/Genrative-Ai-Agentic-Ai-`, and select the branch containing this project.
3. Confirm the `epfosathi` web service from `render.yaml` and deploy it. The Docker image seeds the six starter records on each fresh container start.
4. Copy the real Render URL (for example, `https://genrative-ai-agentic-ai-2.onrender.com/`) into the **Live deployment URL** fields in this README and `TRACKER.md`. Do not use the example URL as if it were real.
5. Verify publicly: `https://YOUR-REAL-RENDER-URL/health` must return HTTP 200 and `{"status":"ok","service":"EPFOSathi"}`. Record the check date in `TRACKER.md`.

**Storage note:** The included Render free-plan configuration uses the container's local filesystem. SQLite data may be reset when the service is replaced or restarted. The six bundled knowledge records are re-seeded at startup; records created through the API are not guaranteed to persist. For persistent user-created records, attach a paid persistent disk and set `DATABASE_PATH` to a path on that disk.

**Deployment status:** Not deployed from this workspace. The live URL remains pending until you deploy it in your Render account and verify `/health`.

## S1 delivery: CI and feature-branch pull request

GitHub Actions runs Ruff, pytest, and a Docker image build on pushes and pull requests. The badge at the top reports the `main` branch workflow status. A green badge alone does not prove the required feature-branch PR was merged; record the actual PR URL and merge commit in `TRACKER.md`.

Example PowerShell workflow (run from the repository root):

```powershell
git checkout -b feature/epfosathi-ci-deploy
git add .
git commit -m "Add EPFOSathi CI and deployment configuration"
git push -u origin feature/epfosathi-ci-deploy
```

Open a pull request from `feature/epfosathi-ci-deploy` into `main` on GitHub. Wait until the Ruff, pytest, and Docker build checks are all green, then merge the PR. Update `TRACKER.md` with the PR URL, merge date, and merge commit SHA. Do not mark S1 complete before that evidence exists.

## Project layout

```text
EPFOSathi/
├── app/
│   ├── agent.py
│   ├── config.py
│   ├── database.py
│   ├── llm.py
│   ├── main.py
│   ├── repository.py
│   ├── schemas.py
│   └── static/index.html
├── data/seed.json
├── scripts/
│   ├── __init__.py
│   └── seed.py
├── tests/
├── .env.example
├── Dockerfile
├── render.yaml
└── README.md
```
