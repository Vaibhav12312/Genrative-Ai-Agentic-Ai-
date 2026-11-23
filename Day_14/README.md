# EPFOSathi — Interview Handover Pack

EPFOSathi is an informational assistant concept for helping EPF members navigate official Employees' Provident Fund Organisation (EPFO) guidance. Its core design principles are source-grounded retrieval, transparent provenance, careful handling of overlapping FAQ records, deterministic date calculations and safe fallback when evidence is insufficient.

> **Scope note:** Day 13 app is included. The expanded dataset contains 320 input records: 20 user-supplied EPFO FAQ records and 300 model-generated draft records. The deduplication build produces 317 canonical records and 3 review-queue entries. The generated records are not official EPFO publications and require record-by-record source and policy verification before production use.

## Package contents

```text
EPFOSathi/
├── README.md
├── PROGRESS.md
├── data/
│   └── sample_records.py
├── docs/
│   └── interview.md
├── scripts/
│   └── verify_handover.py
└── tests/
    └── test_interview_docs.py
```

## Interview preparation

Open [`docs/interview.md`](docs/interview.md) for:

- A concise 60-second pitch.
- Ten likely technical/product interview questions and suggested answers.
- The hardest-problem story in STAR format.
- A 3–4 minute demo walkthrough and rehearsal record.

## Verify this handover

Requires Python 3.10+; the checks use only the Python standard library.

```bash
pytest -q
python scripts/build_kb.py
python scripts/verify_handover.py
python scripts/rehearse_demo.py
```

The test suite validates the API and core helper behavior. The rehearsal script runs two API-level smoke walkthroughs against temporary databases. These checks do **not** validate the completeness of the 300+ FAQ corpus, retrieval quality across that corpus, the current legal/policy correctness of date-rule parameters, or a human-operated browser demo.

## FAQ data and provenance

The dataset file is `data/sample_records.py`. It contains 320 input records: 20 user-supplied FAQ records and 300 model-generated draft records. Each generated record is marked `source_type=model_generated_from_general_epfo_scheme_knowledge` and `verification_status=draft_requires_official_review`. Its `source_url` is a research reference, not proof that the linked page contains or verifies that exact answer. The generated records must not be presented as official EPFO answers. Before production use:

1. Collect records from the official EPFO sources and retain the original URL.
2. Store publication/update date separately from crawl time and last-verified date.
3. Detect exact and near-duplicate candidates, then review meaning and conditions before merging.
4. Prefer the newest verified official guidance; flag unresolved conflicts for human review.
5. Keep historical records labelled as historical rather than silently rewriting them.
6. Re-test retrieval and date calculations after every knowledge-base update.

## Production and safety notes

- EPFOSathi is not an official EPFO service and must not imply government affiliation.
- Do not present an answer as current without a source and verification date.
- Do not let the LLM independently calculate statutory dates or infer missing eligibility facts.
- Do not invent claim status, form applicability, URLs, deadlines or exceptions.
- Escalate case-specific or disputed matters to official EPFO channels.
- Do not log UAN, Aadhaar, bank details, claim identifiers or other unnecessary personal data.

## Progress and release status

See [`PROGRESS.md`](PROGRESS.md). See PROGRESS.md for what is open.

## Official references

- https://www.epfindia.gov.in/
- https://www.epfindia.gov.in/site_en/FAQ.php
- https://unifiedportal-mem.epfindia.gov.in/memberinterface/

Always re-check current official guidance before relying on a form name, deadline or portal route.
