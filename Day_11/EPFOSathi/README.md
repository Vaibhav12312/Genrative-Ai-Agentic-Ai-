# EPFOSathi

EPFOSathi is a small, runnable EPF/EPFO information assistant. It provides a FastAPI backend, a responsive browser UI, SQLite-backed knowledge records, keyword search, and a tool-using question-answer agent. The default answer provider is local and deterministic; no API key or paid LLM is required to run the project.

> **Important scope note:** The available task brief in this conversation specifies S1 and S2 acceptance criteria, but does not include a fuller product specification or original starter repository. This implementation therefore provides a complete baseline for those stated requirements. The seeded content is general informational guidance, not live EPFO data or official advice.

## Features

- `GET /health` health status and record count.
- `GET /api/records` list all knowledge records.
- `GET /api/records/{record_id}` retrieve one record.
- `GET /api/search?q=...&limit=...` case-insensitive AND-term search with common question words ignored.
- `POST /ask` retrieve relevant records using the `search_epf_records` agent tool and generate an answer through an injectable LLM interface.
- Browser UI at `/` for asking questions and searching the knowledge base.
- SQLite persistence with starter records seeded on first run.
- Safe fallback response when the knowledge base has no relevant match.

## Requirements

- Python 3.11 or newer (Docker uses Python 3.12).
- Docker Engine and Docker Compose plugin for container execution.

## Run locally

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open <http://127.0.0.1:8000>. Interactive API documentation is at <http://127.0.0.1:8000/docs>.

## Run with Docker

From the project root (the directory containing `Dockerfile` and `docker-compose.yml`):

```bash
docker compose up --build
```

Then open <http://localhost:8000>. The API and UI are served by the same EPFOSathi container. SQLite data is stored in the named Docker volume `epfosathi_data`, so it survives container recreation. To stop the service:

```bash
docker compose down
```

To remove the persisted database volume as well (destructive):

```bash
docker compose down -v
```

## API examples

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/records
curl "http://localhost:8000/api/search?q=claim"
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"How can I check my PF claim status?"}'
```

## Tests and lint

Install the development/test dependencies from `requirements.txt`, then run:

```bash
pytest
ruff check .
```

The test suite includes 18 pytest cases covering record listing/retrieval, missing records, search behavior and limits, `/health`, records/search API routes, not-found and validation responses, the UI route, `/ask` with an injected fake LLM, the agent's knowledge tool, and the no-match fallback.

## Project structure

```text
EPFOSathi/
├── app/
│   ├── __init__.py
│   ├── agent.py           # Tool + injectable LLM + agent orchestration
│   ├── main.py            # FastAPI routes and UI hosting
│   ├── records.py         # SQLite repository and starter knowledge
│   └── static/index.html  # Browser UI
├── tests/
│   ├── conftest.py
│   ├── test_agent.py
│   ├── test_api.py
│   └── test_records.py
├── .dockerignore
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Configuration and extension points

- `EPFOSATHI_DB` selects the SQLite database path. Default: `./data/epfosathi.db`.
- Replace `GroundedFallbackLLM` with a provider implementation that satisfies `generate(question, context) -> str`; inject it into `EPFAgent`. Keep secrets in environment variables and never commit API keys.
- Add or update knowledge entries in `DEFAULT_RECORDS` in `app/records.py` (or add an authenticated admin/import workflow before production use).
- Search is intentionally simple keyword matching, not semantic/vector search.

## Privacy and production notes

Do not submit UAN, Aadhaar, PAN, bank account details, passwords, OTPs, or other personal identifiers. This baseline does not authenticate users, access EPFO systems, submit claims, or retrieve private member data. Before public deployment, add authentication and rate limiting if required, HTTPS/reverse proxy configuration, operational logging, backup/restore procedures, dependency review, and content review against current official EPFO guidance. Do not represent this application as an official EPFO service.
