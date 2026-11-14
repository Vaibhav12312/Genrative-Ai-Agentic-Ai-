# EPFOSathi Prompt Version 1 — Individual Evaluation Report

**Report type:** Prompt-design preview (not a live model evaluation)  
**Prompt:** `prompts/task_v1.md`  
**Shared system prompt:** `prompts/system.md`  
**Question set:** `eval/questions.json` (10 questions)

> Important: This report is an individual companion copy of the comparison notes. It does not contain invented model responses, latency measurements, or scores. Run `python -m eval.run_eval` with a valid Groq/Gemini API key to generate actual results.

## Prompt profile

Version 1 is the minimal task instruction. It gives the model broad EPFO-helpdesk direction but fewer constraints on response structure, confidence calibration, follow-up questions, and edge cases.

## Review checklist for the 10 questions

| Q | Question focus | What the reviewer should verify |
|---|---|---|
| 1 | First-time UAN activation | Correct official process; never ask the user to share an OTP or password. |
| 2 | EPF vs EPS | Clear distinction between provident-fund savings and pension scheme. |
| 3 | Check PF balance | Directs the user to official EPFO member/passbook services. |
| 4 | Full withdrawal after leaving job | Avoids guaranteeing eligibility; explains that rules depend on circumstances and current EPFO rules. |
| 5 | Transfer PF to a new employer | Gives a safe transfer outline without requesting credentials. |
| 6 | Exact personal PF balance | Clearly admits it cannot access the user's passbook or private contribution data. |
| 7 | Correct date of birth | Gives a cautious correction route and avoids unsupported guarantees. |
| 8 | Current EPF interest rate | Treats the rate as time-sensitive and points to an official current source. |
| 9 | Withdraw PF to invest | Avoids personalized investment advice and presents neutral considerations. |
| 10 | Cricket prediction | Politely identifies the request as outside EPFOSathi's scope and redirects. |

## Expected strengths and risks (prompt-design assessment)

- **Strength:** Short instruction leaves room for natural responses.
- **Risk:** Output structure may vary between questions.
- **Risk:** Confidence values may not be consistently calibrated.
- **Risk:** Follow-up questions may be missing or generic.
- **Risk:** Time-sensitive and out-of-scope questions may receive less consistent handling than with the structured prompt.

## Live evaluation status

**Not run in this report.** No API call has been represented as completed. For measured results, run the evaluation script and review the generated answer for each question. Score the actual responses in `eval/manual_scorecard.csv`.
