# EPFOSathi — Day 14 Progress and Release Checklist

Last updated: 2026-11-23

## Verified automatically in the uploaded workspace

| Item | Status | Evidence |
|---|---|---|
| Day 13 application included | DONE | `app/`, Docker files, CI workflow and API tests are present |
| 60-second pitch and 10 interview Q&A | DONE | `docs/interview.md` |
| Hardest-problem STAR story | DONE | `docs/interview.md`; accurately distinguishes supplied records from generated drafts |
| FAQ normalization, deduplication and canonical selection | DONE for current sample | `app/services/dedupe.py`; `scripts/build_kb.py` |
| Outdated URL/form heuristic | DONE as a heuristic only | `is_outdated()` and tests; this is not a policy audit |
| Date arithmetic implemented outside the LLM | DONE technically | `app/services/datetools.py`; expanded boundary tests |
| Knowledge-base build | DONE | 320 inputs -> 317 canonical records + 3 review-queue entries |
| Automated tests | PASS | `pytest -q` -> 32 passed before this update; rerun after changes |
| Handover verifier | PASS | `python scripts/verify_handover.py` |
| Automated API rehearsals | PASS | `python scripts/rehearse_demo.py` -> two API smoke runs passed; `database.connect()` now explicitly closes SQLite connections to avoid Windows temp-file cleanup failures |
| Final tag in local Git metadata | EXISTS LOCALLY | `v1.0.0-final`; tag is not proof of a remote release |

## Remaining actions — do not mark complete until performed

| Item | Status | Required action |
|---|---|---|
| Verify 36-month, 2-month and 6-month rule policy values | OPEN — official policy review | Confirm each rule, conditions and exceptions against current official EPFO material. The code currently returns `verify: true` for the 36-month rule; date arithmetic passing tests does not validate the policy. Keep the warning until reviewed. |
| Verify all FAQ source content, URLs and claim-form references | OPEN — source review | The corpus has 320 records, but only 20 are user-supplied EPFO FAQ text. The other 300 are model-generated drafts. Verify each draft against the exact current official source, retain a checked date, and revise/remove unsupported entries. Do not claim that 300+ official FAQs have been collected. |
| Human-operated browser demo twice | OPEN — user action | Run the two browser rehearsals using the checklist in `docs/interview.md`; record date, browser, result and any issues for each run. Automated API rehearsals are not browser rehearsals. |
| Ruff lint | FIXED IN SOURCE; rerun locally | Fixed all four reported findings: two E402 import annotations and two import-order issues. Ruff is not installed in this packaging runtime, so confirm with `python -m ruff check .` in the user's environment. |
| Push final commit and tag to GitHub | OPEN — repository owner action | No Git remote is configured in the supplied archive. Add the intended remote, inspect it, commit the reviewed changes, then push branch and tag. Never push to an unverified URL. |

## Data integrity and interview wording

- `data/sample_records.py` contains 320 inputs: 20 user-supplied EPFO FAQ records and 300 model-generated draft records.
- Generated records use `source_type=model_generated_from_general_epfo_scheme_knowledge` and `verification_status=draft_requires_official_review`. Their URLs are research references, not evidence that the exact answer appears there.
- The latest build reports 317 canonical records and 3 review-queue entries.
- Zero records flagged by the URL/form heuristic does not prove current policy accuracy.
- Similarity grouping creates candidates; human review must preserve differences in conditions, eligibility and claim type.
- The date-tool functions perform deterministic calendar arithmetic. The configured 36/2/6-month policy assumptions still need official-source verification.
- The application currently uses `FakeLLM`; do not describe it as a production LLM integration.
- EPFOSathi is an informational project, not an official EPFO service.

## Release decision

**Local code handover: conditionally ready. Full Day 14 acceptance: NOT COMPLETE.**

The local tests and automated API rehearsals pass in the supplied archive. Official-source verification, two human browser demos, Ruff execution and GitHub push remain owner actions. Do not close these items by assumption.
