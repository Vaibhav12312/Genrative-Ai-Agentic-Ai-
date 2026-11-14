# EPFOSathi Prompt Version 2 — Individual Evaluation Report

**Report type:** Prompt-design preview (not a live model evaluation)  
**Prompt:** `prompts/task_v2.md`  
**Shared system prompt:** `prompts/system.md`  
**Question set:** `eval/questions.json` (same 10 questions as Version 1)

> Important: This report is an individual companion copy of the comparison notes. It does not contain invented model responses, latency measurements, or scores. Run `python -m eval.run_eval` with a valid Groq/Gemini API key to generate actual results.

## Prompt profile

Version 2 uses explicit instructions for concise answers, ordered steps, confidence bands, follow-up questions, time-sensitive EPFO information, and out-of-scope requests.

## Review checklist for the 10 questions

| Q | Question focus | What the reviewer should verify |
|---|---|---|
| 1 | First-time UAN activation | Gives a concise sequence using official services; never asks for OTP/password. |
| 2 | EPF vs EPS | Clearly compares the provident-fund and pension components without conflating them. |
| 3 | Check PF balance | Gives a short, usable route to the official member portal/passbook. |
| 4 | Full withdrawal after leaving job | Makes eligibility conditional and avoids promising a full withdrawal. |
| 5 | Transfer PF to a new employer | Provides clear steps and avoids collecting sensitive login information. |
| 6 | Exact personal PF balance | Explicitly states that it cannot see the user's private passbook or exact contributions. |
| 7 | Correct date of birth | Provides a cautious correction route and flags that requirements can change. |
| 8 | Current EPF interest rate | Does not present an unverified rate as current; directs the user to official updates. |
| 9 | Withdraw PF to invest | Gives neutral considerations, not individualized investment instructions. |
| 10 | Cricket prediction | Declines the unrelated prediction and redirects to EPFO/PF assistance. |

## Expected strengths and risks (prompt-design assessment)

- **Expected strength:** Consistent direct-answer-first structure and concise steps.
- **Expected strength:** More explicit confidence guidance, especially when private data is unavailable.
- **Expected strength:** Clearer handling of current information and out-of-scope requests.
- **Trade-off:** More prescriptive instructions may make some answers feel formulaic or slightly longer.
- **Verification needed:** Check whether the model follows the word limit, confidence rubric, and safety instructions in practice.

## Live evaluation status

**Not run in this report.** No API call has been represented as completed. For measured results, run the evaluation script and review the generated answer for each question. Score the actual responses in `eval/manual_scorecard.csv`.
