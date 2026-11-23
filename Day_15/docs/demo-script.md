# EPFOSathi – 5-Minute Live Demo Script

## 0:00–0:40 | Introduction
“Hello. My project is EPFOSathi, an AI-assisted assistant for common EPFO and Employees’ Provident Fund questions.

The problem I focused on is that EPFO information can be difficult for users to navigate. Similar questions may have overlapping answers, and older information can contain outdated portal links or form references. My goal was to make common information easier to find while keeping account-specific actions on official EPFO channels.”

## 0:40–1:30 | Problem and solution
“During preparation, I worked with more than 300 short FAQ entries from two EPFO websites. Some entries were duplicates or near-duplicates, and some answers needed checking because URLs, forms, or date rules could change.

EPFOSathi organizes this information and provides a simple question-and-answer experience. It is an information assistant, not a replacement for the official EPFO portal.”

## 1:30–3:45 | Live demonstration
1. Open the deployed URL.
2. Show the home page and explain the main user flow.
3. Enter: **What is a Universal Account Number (UAN)?**
4. Explain the response in plain language.
5. Ask one other question that you have personally verified against the current knowledge base.
6. If available, show the relevant FAQ/search or source-handling feature.
7. Show the safe fallback for account-specific requests: users are directed to the official EPFO member portal.

**Demo safety:** Use only test/example questions. Do not enter real UANs, passwords, Aadhaar numbers, bank details, or other personal information.

## 3:45–4:30 | Technical overview
“Behind the interface, the project uses a curated FAQ data source and application logic to retrieve and present relevant information. I also added validation and tests to check important behavior. The project’s automated test run completed with 32 passing tests, and the handover checks validated 320 FAQ input records.”

Only name frameworks, databases, APIs, or deployment services that are actually present in your repository.

## 4:30–5:00 | Closing
“One important lesson was that an answer assistant must not only produce an answer; it must also handle uncertain or account-specific requests responsibly. EPFOSathi provides general information and directs users to official channels when personal account access is required. Thank you. I’m ready for questions.”

## Before presenting
- Replace/use the actual deployed URL.
- Confirm the two demo questions work in the live deployment.
- Keep the GitHub repository and README open in another tab.
- Rehearse with a timer; target 4:45–5:00.
