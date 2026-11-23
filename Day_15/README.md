# Day 15 – EPFOSathi Final Test & Demo Day

## Objective
Complete the 45-minute final test and deliver a clear, reliable 5-minute live demonstration of EPFOSathi, followed by a 3-minute Q&A.

## Project overview
EPFOSathi is an AI-assisted information assistant for common Employees' Provident Fund (EPF/EPFO) questions. It helps users find understandable answers from a curated FAQ knowledge base and directs users to official EPFO channels for account-specific actions.

## What to demonstrate
1. Open the deployed live URL and show that the application loads.
2. Ask a common question, for example: **“What is a Universal Account Number (UAN)?”**
3. Show how the assistant responds with general EPFO information.
4. Demonstrate one more representative FAQ or search flow.
5. Explain that account-specific status and transactions must be handled through the official EPFO member portal.
6. Briefly show the project README/repository and explain the main components.

## Known project validation evidence
The latest project work recorded:
- Automated test suite: **32 passed**.
- Handover validation: **320 FAQ input records validated**.
- URL checks were reported as returning the expected output.
- A records endpoint returned `{"items":[],"count":0}` during one check; explain this accurately if asked. Do not describe it as a failure unless you have confirmed it was unexpected for that endpoint.

Use the latest actual deployment and test results during the presentation. Do not claim a deployment is live until you have opened and tested the live URL.

## Demo-day deliverables
- Live deployed URL
- Project README
- One real failure/issue, its root cause, fix, and measured result

## Suggested final preparation
- [ ] Confirm the live URL opens in a fresh browser session.
- [ ] Test two representative questions.
- [ ] Confirm the fallback response is safe and understandable.
- [ ] Keep the repository and README ready to show.
- [ ] Rehearse the 5-minute script in `docs/demo-script.md`.
- [ ] Review likely questions in `docs/interview-qa.md`.
- [ ] Complete `docs/failure-analysis.md` with the exact issue and evidence from your own run.
