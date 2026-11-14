Task: answer the employee's EPFO question below.

How to write the "answer":
- Start with a one-sentence direct answer.
- If the task has a process, give short numbered steps (max 5) inside the string, using "1)", "2)" ...
- Mention any document or prerequisite they need (for example an active UAN or completed KYC) only if you are sure it applies.
- If the question depends on rules or numbers that change over time, say that clearly and point to the official EPFO member portal or epfindia.gov.in instead of quoting a figure.
- If the question is out of scope, say so in one sentence and offer an EPFO-related alternative.
- Keep it under 140 words.

How to set "confidence" (be honest, do not default to a high value):
- 0.85-1.0: stable, well-known process or concept
- 0.55-0.84: generally right but details may differ by case or have changed
- 0.2-0.54: time-sensitive, case-specific or you are unsure
- 0.0-0.19: out of scope or you cannot answer

How to set "follow_up": ask ONE specific question that would let you help further (for example whether their UAN is already active), or suggest the single best next step.

Example (format only):
{"answer": "Short direct answer. 1) Step one. 2) Step two.", "confidence": 0.8, "follow_up": "Is your KYC already complete?"}

Employee's question: {question}

Return only the JSON object.
