# One Failure Fixed – Evidence-Based Story

Complete this page with an issue you personally observed in EPFOSathi. A strong answer explains the symptom, root cause, fix, and measurable evidence.

## Suggested issue to investigate
During earlier validation, a question such as:

> What is a Universal Account Number (UAN)?

returned a generic fallback response:

> I can help with general EPFO information. You asked: What is a Universal Account Number (UAN)? For account-specific status or action, use the official EPFO member portal.

This may indicate that the question was not matched to the expected FAQ record. Confirm the exact cause from your code, logs, and test data before presenting it as the failure you fixed.

## Fill in the verified details

- **Observed failure:** [What did the user see? Include the exact input and output.]
- **Expected behavior:** [What should EPFOSathi have returned?]
- **Root cause:** [For example, retrieval/matching logic, data normalization, missing record, or configuration. Use only the cause you confirmed.]
- **Fix made:** [Name the file/function or data change and explain what changed.]
- **How it was measured:** [Name the test, command, endpoint, or before/after comparison.]
- **Before:** [Record the failing output or test result.]
- **After:** [Record the corrected output or passing test result.]

## Evidence already recorded (project validation)
- Automated tests: **32 passed**.
- Handover checks: **320 FAQ input records validated**.
- A records endpoint returned `{"items":[],"count":0}` in one check. Determine whether this was expected for the queried dataset before describing it as a defect.

## 30-second interview answer template
“One issue I investigated was [specific failure]. The expected result was [expected behavior], but I observed [actual behavior]. I traced it to [confirmed root cause]. I fixed it by [specific change]. I verified the fix using [test/command] and measured the result as [before → after]. This gave me confidence that the issue was resolved without breaking the other tested behavior.”

**Important:** Do not present the suggested UAN fallback example as a successfully fixed bug unless you have verified that the behavior was wrong, made a fix, and reproduced the corrected result.
