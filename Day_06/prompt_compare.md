# EPFOSathi Prompt Comparison Report



## 1. Objective

Compare two EPFOSathi prompt versions (V1 and V2) using the same 10
representative Employees' Provident Fund (EPF) questions.

## 2. Prompt versions

- **V1:** Basic EPFO assistant prompt that provides a direct answer and a short follow-up.
- **V2:** Structured EPFO assistant prompt that prioritizes clear steps, avoids unsupported certainty, and asks for missing details when needed.

## 3. Test questions

1. What is a UAN?
2. How can an employee check their EPF passbook?
3. How can I activate my UAN?
4. What should I do if my PF transfer claim is pending?
5. How can I update my mobile number linked to UAN?
6. What is Form 19 used for?
7. What is Form 10C used for?
8. How can I check my PF claim status?
9. What should I do if my employer has not deposited PF?
10. Can I withdraw my PF after leaving a job?

## 4. Illustrative comparison

| # | Topic | V1 illustrative result | V2 illustrative result | Sample preference |
|---:|---|---|---|---|
| 1 | UAN meaning | Defines UAN briefly | Defines UAN and explains its purpose | V2 |
| 2 | Passbook | Gives a short portal instruction | Gives ordered login and navigation steps | V2 |
| 3 | UAN activation | Lists basic activation steps | Lists steps and notes details needed to activate | V2 |
| 4 | Pending transfer | Suggests checking claim status | Suggests checks and explains when escalation may be needed | V2 |
| 5 | Mobile update | Gives a general update instruction | Separates profile update and verification steps | V2 |
| 6 | Form 19 | Says it is for PF final settlement | Explains its purpose and distinguishes it from pension withdrawal | V2 |
| 7 | Form 10C | Says it relates to pension benefits | Explains its use and notes eligibility can matter | V2 |
| 8 | Claim status | Directs user to the claim-status page | Gives a clearer sequence of portal steps | V2 |
| 9 | Employer non-deposit | Advises contacting the employer | Suggests checking passbook records and appropriate grievance steps | V2 |
| 10 | Leaving a job | Gives a general withdrawal answer | Explains that eligibility and waiting-period rules may apply | V2 |

## 5. Sample scoring rubric

Score each response from 1 (poor) to 5 (excellent).

- **Accuracy:** Is the information correct and appropriately qualified?
- **Completeness:** Does it address the user's question?
- **Clarity:** Is the answer easy to understand and follow?
- **Safety:** Does it avoid inventing EPFO rules, guarantees, or account details?

| Criterion | V1 sample score | V2 sample score |
|---|---:|---:|
| Accuracy | 3.5 / 5 | 4.0 / 5 |
| Completeness | 3.2 / 5 | 4.2 / 5 |
| Clarity | 3.8 / 5 | 4.3 / 5 |
| Safety | 3.4 / 5 | 4.2 / 5 |
| **Illustrative average** | **3.48 / 5** | **4.18 / 5** |

## 6. Sample conclusion

In this illustrative comparison, V2 is preferred because its structured format
provides clearer steps, better qualification of eligibility-dependent answers,
and more explicit handling of missing information. 


## 8. Evaluation status

- [ ] 20 live model responses generated successfully
- [ ] All 10 questions reviewed for both V1 and V2
- [ ] Scores replaced with reviewer-assigned values
- [ ] Final conclusion based on actual outputs


