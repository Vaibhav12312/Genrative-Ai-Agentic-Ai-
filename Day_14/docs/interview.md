# EPFOSathi — Interview Preparation

> **Positioning:** EPFOSathi is an explainable, retrieval-first assistant for common Employees' Provident Fund (EPF) and Employees' Pension Scheme (EPS) questions. It helps members find relevant guidance from official EPFO material, understand the next step, and identify when an answer needs confirmation from EPFO.
>
> **Important:** EPF rules, forms, portal paths and eligibility conditions can change. This project is an information assistant, not an official EPFO service or a substitute for advice from EPFO. Always show the source and its last-verified date; direct users to official channels for case-specific decisions.

## 1. 60-second pitch

“EPF information is spread across official pages, FAQs and service portals. A member may find several answers to what looks like the same question, but those answers can differ because one is old, one refers to a previous form, or one points to an outdated portal URL. That makes a simple task—like understanding a claim or transfer—confusing.

EPFOSathi is designed to make that information easier to navigate. It retrieves relevant answers from a curated knowledge base, keeps source references with the answer, and uses deterministic tools for calculations and date-based rules instead of asking a language model to guess. The knowledge pipeline also normalizes and deduplicates near-identical FAQs, while preferring the newest verified source when versions conflict.

The goal is not to replace EPFO or make legal decisions. It is to give members a clearer first explanation, show where the information came from, and guide them to the official EPFO channel when their situation needs confirmation.”

## 2. Ten likely interview questions and suggested answers

### Q1. What problem does EPFOSathi solve?

**Answer:** EPFO information is distributed across multiple official pages and portals. Similar questions can have overlapping answers, and older content may mention outdated URLs or forms. EPFOSathi makes the first step easier by retrieving relevant, source-backed information from a curated knowledge base and clearly flagging uncertainty or information that needs official confirmation.

### Q2. Why did you build a retrieval-based assistant instead of relying only on an LLM?

**Answer:** A model answering from memory can confidently produce stale or unsupported information. Retrieval grounds the response in the project’s collected EPFO material. The answer can include source details, and the model is instructed not to invent a rule when the retrieved material does not support it. Deterministic calculations and date rules are handled by code rather than generated text.

### Q3. What was the hardest engineering problem?

**Answer:** The hardest problem is consolidating a large FAQ corpus collected from multiple EPFO web sources. Many questions overlap or are near-duplicates, while some answers may be outdated—for example, old portal URLs or older claim-form references where the Composite Claim Form may now apply. The challenge is to deduplicate carefully without deleting meaningful differences, retain the newest verified version, and avoid letting the LLM calculate date-dependent eligibility. I normalize text, compare likely duplicates, retain provenance and verification status, and route date calculations through deterministic tools. In this Day 14 dataset, 20 records came from the FAQ text supplied for the project and 300 additional records are model-generated drafts awaiting official review; they are not 300 independently collected official FAQs.

### Q4. How did you handle duplicate or near-duplicate FAQs?

**Answer:** I treat deduplication as a reviewable data-quality step, not simply deleting records with similar wording. First, normalize whitespace, punctuation and common wording variations. Then use exact matching and similarity-based candidate grouping to find likely duplicates. A reviewer compares the question intent, answer, source, applicable form and effective/verification date. Truly equivalent records are consolidated; records with different conditions remain separate. The canonical record keeps source provenance and a history or reference to the alternatives.

### Q5. How do you decide which answer is the newest and most trustworthy?

**Answer:** Source authority and freshness are both important. Official EPFO material takes precedence over unofficial summaries. Among official records, prefer the newest verifiable publication or update date, while retaining the URL and the date checked. If dates are missing or two official sources conflict, do not silently guess: mark the record for review and explain the uncertainty. A crawl or file timestamp alone should not be treated as the policy effective date.

### Q6. Why calculate date rules with a tool instead of the LLM?

**Answer:** Date rules need repeatable arithmetic and explicit boundary handling. A deterministic function can parse dates, apply the documented rule, handle leap years and invalid inputs, and be tested against fixed examples. The LLM can explain the result in plain language, but it should not invent dates or perform the authoritative calculation. The rule itself must be sourced, versioned and reviewed when EPFO guidance changes.

### Q7. How do you prevent outdated forms or portal links from appearing as current guidance?

**Answer:** Store form names, URLs, source dates and verification status as structured metadata. Before a record is published, check its official source and confirm whether the referenced form or portal route is still current. Historical information can remain available when useful, but it must be labelled historical and must not be presented as the current process. For claim guidance, the knowledge base should distinguish older form references from the Composite Claim Form where applicable, and avoid implying that one form applies to every claim type.

### Q8. What happens when the knowledge base does not contain the answer?

**Answer:** The assistant should say that it could not find a sufficiently supported answer. It can ask a focused clarifying question or point the member to the relevant official EPFO service. It should not fill the gap with a plausible-sounding answer. High-impact or case-specific questions—such as disputed service history, rejected claims or eligibility exceptions—should be referred to EPFO for confirmation.

### Q9. How would you test and monitor EPFOSathi?

**Answer:** I would test the data pipeline, duplicate grouping, retrieval relevance, source attribution, date-tool boundaries, input limits and API error handling. For the assistant, I would maintain a small evaluation set of representative questions, including ambiguous questions, conflicting FAQ versions, outdated URLs and prompt-injection attempts. In production, monitor latency, token usage, cache hit rate, retrieval failures, unanswered questions and user feedback. Re-run the evaluation set whenever the knowledge base or prompt changes.

### Q10. What would you improve next?

**Answer:** I would add a repeatable source-refresh workflow with change detection, human approval for policy-sensitive updates, stronger retrieval evaluation, and a visible “last verified” label on every answer. I would also expand the test set with real anonymized member questions and measure whether the retrieved source actually supports each answer. The priority is trustworthy guidance, not merely more conversational features.

## 3. Hardest-problem story — STAR format

- **Situation:** The target EPFOSathi knowledge base needed to handle 300+ short FAQs from EPFO sources. Similar questions can overlap, while older records may contain legacy portal paths or claim-form instructions.
- **Task:** Build a searchable corpus and deduplicate it without losing meaningful differences or presenting generated or outdated material as verified official guidance.
- **Action:** Preserve the 20 FAQ records supplied for this project; create 300 additional draft FAQ records across 16 member-service categories; label generated records separately; normalize and group likely duplicates; retain source references and review status; move date arithmetic into deterministic application code with tests.
- **Result:** The build currently processes 320 input records into 317 canonical records and places 3 duplicate/conflict groups in the review queue. This proves the pipeline runs on the expanded dataset, not that the 300 generated drafts are official or policy-verified.

**Be precise about delivery status:** only 20 records were supplied as EPFO FAQ text. The other 300 are model-generated draft FAQs, with official EPFO URLs provided as research references, and still require record-by-record source verification before production use. Do not describe them as 300 FAQs collected from two official websites.

## 4. Demo walkthrough (target: 3–4 minutes)

1. **Start the service:** Show the documented local run command and confirm the health endpoint responds.
2. **Explain the knowledge base:** Show one FAQ record and its category, question, answer and official source URL.
3. **Ask a common question:** Enter a representative EPF question. Show the retrieved source and explain that the response is grounded in it.
4. **Show duplicate handling:** Demonstrate two similar FAQ records grouped for review; explain why conditions and source dates must be checked before merging.
5. **Show a date-rule tool:** Use a fixed test case and show that application code returns the date result. Explain that the LLM only communicates the result.
6. **Show safe fallback:** Ask an unsupported or ambiguous question and demonstrate that the assistant asks for clarification or points to an official channel instead of guessing.
7. **Close:** Reiterate that EPFOSathi is an informational assistant, not an official EPFO service.

**Demo safety:** Use synthetic or public FAQ examples. Never display a real member's UAN, Aadhaar, bank details, claim ID, phone number or other personal data.

## 5. Rehearsal record

| Run | What was exercised | Result |
|---|---|---|
| Automated API rehearsal 1 | Home page, health endpoint, FAQ question, deterministic date tool, missing-input validation | All 5 checks passed using FastAPI TestClient |
| Automated API rehearsal 2 | Repeated the same flow with a fresh temporary SQLite database | All 5 checks passed; repeated `/ask` also exercised the cache path |
| Automated test suite | Full unit and API test suite | `pytest -q`: 32 passed |
| Knowledge-base build | `python scripts/build_kb.py` | 320 input records in, 317 canonical, 3 review-queue entries; 0 flagged by the URL/form heuristic (not a policy audit) |

Repeat both API rehearsals with `python scripts/rehearse_demo.py`. These are automated API-level smoke rehearsals, not two human-operated browser demos.

### Human-operated browser rehearsal log — complete on your computer

Start the application from the repository root with `uvicorn app.main:app --reload`, then open `http://127.0.0.1:8000`. Complete all seven walkthrough steps above twice. Do not pre-fill this log: enter the actual date and outcome after each live run.

| Run | Date/time | Browser | Seven steps completed? | Issues / fixes |
|---|---|---|---|---|
| Browser rehearsal 1 | Pending user entry | Pending | Pending | Pending |
| Browser rehearsal 2 | Pending user entry | Pending | Pending |

A run counts only after you personally operate the application in a browser and verify the visible responses. The two automated API rehearsals in the table above do not satisfy this requirement.

**Dataset limitation:** this archive now contains 320 input records, but only 20 were supplied as EPFO FAQ text. The remaining 300 are model-generated drafts and need record-by-record official verification. Do not say the full corpus was collected from two EPFO websites or is policy-audited. The date-tool code is deterministic, but its 36-month, 2-month and 6-month policy parameters still require current official-source verification.

## 6. Useful official references

- EPFO official website: <https://www.epfindia.gov.in/>
- EPFO FAQ portal: <https://www.epfindia.gov.in/site_en/FAQ.php>
- EPFO member unified portal: <https://unifiedportal-mem.epfindia.gov.in/memberinterface/>

Check each link and the relevant page before the interview. EPFO may change URLs and procedures; the presence of a URL here is not a guarantee that a particular service route is currently available.
