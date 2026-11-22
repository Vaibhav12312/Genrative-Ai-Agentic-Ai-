# EPFOSathi Delivery Tracker

Last updated: 2026-11-21

Repository: https://github.com/Vaibhav12312/Genrative-Ai-Agentic-Ai-

Live deployment URL: **PENDING — deploy the Render Blueprint and replace this line with the real public URL.**

## S1 — CI and pull request

| Requirement | Status | Evidence / action |
|---|---|---|
| `.github/workflows/ci.yml` | Implemented | Runs on pushes to `main`/`feature/**`, pull requests into `main`, and manual dispatch |
| Ruff | CI configured; local run unavailable here | CI executes `ruff check .`; confirm green result in GitHub Actions |
| Pytest | Passed locally | `17 passed` in this workspace on 2026-11-21 |
| Docker build | CI configured; not run locally | CI executes `docker build --pull`; Docker is not installed in this workspace |
| Green README badge | Configured | Badge links to this repository's `ci.yml` workflow on `main`; verify it turns green after a successful run |
| Feature branch PR | Pending GitHub action | Create `feature/epfosathi-ci-deploy` and open PR into `main` |
| PR merged after CI green | **Not complete** | PR URL: PENDING; merge date: PENDING; merge commit SHA: PENDING |

## S2 — Deployment

| Requirement | Status | Evidence / action |
|---|---|---|
| Render deployment configuration | Implemented | `render.yaml` uses Docker and `/health` health check |
| Docker startup seeding | Implemented | Container runs `python -m scripts.seed` before Uvicorn |
| Public deployment | **Pending** | Deploy the Blueprint from the connected GitHub repository in your Render account |
| Live URL in README | Pending | Add the real public URL after Render deployment |
| Live URL in tracker | Pending | Add the same real public URL here |
| Public `/health` HTTP 200 | Pending | Test `https://YOUR-REAL-URL/health` from a public browser/network |

## Local verification in this workspace

| Check | Result | Notes |
|---|---|---|
| Pytest | PASS | `17 passed` |
| Ruff | NOT RUN | Ruff is declared in `.[dev]`, but this workspace could not install it because package-network access is unavailable |
| Docker build | NOT RUN | Docker CLI is not installed in this workspace; CI is configured to build it on GitHub Actions |

## Windows PowerShell commands

Extract the ZIP and run these commands from the extracted project root (the folder directly containing `pyproject.toml`):

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
python -m scripts.seed
ruff check .
pytest -q
docker build -t epfosathi .
docker run --rm -p 8000:8000 epfosathi
```

For local API-only startup without Docker, use `uvicorn app.main:app --reload` after seeding.

## Remaining actions that require your GitHub/Render account

1. Push this updated project to the repository.
2. Create and push the feature branch `feature/epfosathi-ci-deploy`.
3. Open a PR into `main`; wait for Ruff, pytest, and Docker build to pass.
4. Merge only after CI is green. Record the PR URL, merge date, and merge commit SHA above.
5. In Render, choose **New → Blueprint**, connect this repository, and deploy `render.yaml`.
6. Copy the real Render URL into the Live deployment URL line in both `README.md` and this tracker.
7. Verify the public `/health` endpoint returns HTTP 200 and record the check date.

## Completion rule

S1 is complete only after a feature-branch PR is merged following a green CI run. S2 is complete only after the real public URL is recorded in both README and this tracker and public `/health` returns HTTP 200. Editing a local folder cannot perform or prove those account-level actions.
