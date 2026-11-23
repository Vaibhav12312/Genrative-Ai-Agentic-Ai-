# EPFOSathi – Likely Demo-Day Q&A

Keep answers concise. Be truthful about the implementation; do not claim features that are not in the repository.

## 1. What problem does EPFOSathi solve?
It makes common EPFO information easier to access through a simple question-and-answer interface. It also helps reduce confusion caused by duplicate, overlapping, or outdated FAQ content.

## 2. Who are the target users?
People who need general information about EPF, UAN, claims, forms, and common EPFO processes.

## 3. What was the hardest part?
Working with more than 300 short FAQ records that included overlapping questions and sometimes outdated answers, links, or form references. I had to identify duplicates, prefer the most current reliable information, and validate date-related rules.

## 4. How did you handle duplicate FAQs?
I reviewed similar questions and their answers, grouped near-duplicates, and retained the most appropriate current version rather than treating every wording variation as a separate topic.

## 5. How did you validate the project?
The latest recorded automated test run showed 32 passing tests. The handover checks also validated 320 FAQ input records. I additionally checked the relevant URLs and application responses.

## 6. What happens when a user asks for account-specific information?
The assistant does not claim to access a member’s private EPFO account. It directs the user to the official EPFO member portal for account-specific status or actions.

## 7. Is EPFOSathi an official EPFO application?
No. It is an independent project that helps users understand general EPFO information. Users should rely on official EPFO channels for authoritative updates and account transactions.

## 8. What would you improve next?
I would strengthen source freshness checks, add more verified test cases, improve answer traceability, and monitor the deployed application for errors and outdated information.

## 9. What was one issue you fixed?
Use the real example documented in `failure-analysis.md`. Explain the observed behavior, root cause, exact change, and test or measurement that proves the fix. Do not invent a failure story.

## 10. How would you measure success?
I would track answer correctness against a reviewed test set, retrieval success, fallback accuracy, response time, broken-link rate, and user feedback. For the current project, report only measurements you have actually collected.

## 11. What are the limitations?
The knowledge base may need updates as EPFO rules, forms, and URLs change. The assistant is not a source of private account data and should not replace official EPFO guidance.

## 12. What did you learn?
I learned that data quality, validation, clear fallback behavior, and testing are as important as building the user interface. A useful assistant must communicate its limits honestly.
