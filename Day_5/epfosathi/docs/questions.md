# 10 Real EPFOSathi User Questions

These are typical questions an EPF member asks about UAN, contributions, passbook, transfer, KYC, claims and complaints. The first six cover the core areas and Q6 is the deliberately unanswerable one.
All rows were checked against the running API: see `docs/run_output.txt` and `tests/test_main.py`.
Q6 is the one my data cannot answer.

| # | Question | Can my data answer it? | Matches FAQ id |
|---|----------|------------------------|----------------|
| 1 | What is a UAN and how do I activate it? | Yes | `uan` |
| 2 | How much is deducted from my salary for PF and what does my employer pay? | Yes | `contribution` |
| 3 | How do I check my PF balance? | Yes | `passbook` |
| 4 | How do I transfer my PF when I change my job? | Yes | `transfer` |
| 5 | Why do I need to link Aadhaar and bank account with my UAN? | Yes | `kyc` |
| 6 | **My claim was filed 3 weeks ago and is still pending. When will the money reach my account?** | **No.** It needs live, personal claim status that is not in my static data. | none |
| 7 | Where can I file a complaint against EPFO? | Yes | `grievance` |
| 8 | How do I know whether my employer is actually depositing my PF every month? | Partly (passbook shows deposits, not employer behaviour) | `passbook` |
| 9 | Is my UAN the same when I change companies? | Yes | `uan` |
| 10 | Can I update my bank details if the old account is closed? | Partly (KYC update) | `kyc` |

The original EPFO FAQ records (`app/data/epfo_faq_records.py`) are searched too, but they do not contain
anything about live claim status, so Q6 still falls back.

## Why Q6 cannot be answered
The FAQ is general and static. A pending claim needs the member's live claim record
(status, rejection reason, processing office), which EPFOSathi has no access to. The API
returns `answered: false` and points the user to the portal or grievance system instead of guessing.
