"""EPFO Employee FAQs.

The questions and answers below are the FAQ records used by EPFOSathi.
Each record's source_url points to the EPFO FAQ page they were taken from.
"""

sample_records = [
    {
        "faq_number": 1,
        "category": "Claim & withdrawals",
        "question": "How long an employee will receive interest after he has left employment?",
        "answer": (
            "An employee's EPF account becomes inoperative after 36 months from the date "
            "of his retirement on or after attaining the age of 55 years. The account having "
            "become inoperative stops earning further interest. Accordingly, if the employee "
            "retires on attaining the age of 58 years, the interest will be credited up to "
            "58 years of age. However, in cases where the employee retires voluntarily even "
            "earlier to 55 years, say, 50 years, still the interest will be paid till he attains "
            "the age of 58 as his account becomes inoperative only when he turns 58. In case "
            "the employee retires at the age of 60, then the interest is payable up to 63 years "
            "and so on."
        ),
        "related_form": [],
        "source_url": "https://www.epfo.gov.in/faq-epfo/",
    },
    {
        "faq_number": 2,
        "category": "Claim & withdrawals",
        "question": "Whether a daily rated employee or the piece rated employee can become a member of the EPF?",
        "answer": "Yes",
        "related_form": [],
        "source_url": "https://www.epfo.gov.in/faq-epfo/",
    },
    {
        "faq_number": 3,
        "category": "Claim & withdrawals",
        "question": "If an employee is paid wages on daily basis or on piece rate basis how the contribution is determined?",
        "answer": "The wages paid in a calendar month will be taken to determine the contribution due.",
        "related_form": [],
        "source_url": "https://www.epfo.gov.in/faq-epfo/",
    },
    {
        "faq_number": 4,
        "category": "Claim & withdrawals",
        "question": "Can an employee contribute to the EPF after leaving the service?",
        "answer": (
            "No. In the absence of wages & Employer no recovery can be affected. "
            "Any contribution by the member must be matched with employer’s share of contribution."
        ),
        "related_form": [],
        "source_url": "https://www.epfo.gov.in/faq-epfo/",
    },
    {
        "faq_number": 5,
        "category": "Claim & withdrawals",
        "question": "How a member is informed about the non-payment of contributions recovered from the wages of the employee but not paid to the EPF?",
        "answer": (
            "The Annual P.F. Statement of Account/Member Passbook will indicate the amount "
            "paid by the employer. The default period in a year is thus made known to the "
            "members. In the current scenario if the member has activated her/his UAN the "
            "non-payment/payment of contributions can be verified every month through the "
            "e-passbook. Currently, members also receive sms on their registered mobile phones "
            "on credit of monthly contribution into their PF account."
        ),
        "related_form": [],
        "source_url": "https://www.epfo.gov.in/faq-epfo/",
    },
    {
        "faq_number": 6,
        "category": "Claim & withdrawals",
        "question": "Whether the P.F. amount credited to the member can be attached against any liability?",
        "answer": (
            "No. The Provident Fund enjoys protection against attachment by any Court also "
            "as per the provisions of section 10 of the EPF & MP Act,1952."
        ),
        "related_form": [],
        "source_url": "https://www.epfo.gov.in/faq-epfo/",
    },
    {
        "faq_number": 7,
        "category": "Claim & withdrawals",
        "question": "When wages are not collected by the member whether the PF can be deducted or not?",
        "answer": (
            "The employer, before paying the member his wages, is required to deduct the PF "
            "contribution from his wages and pay to the Regional PF Commissioner. As such "
            "PF can be deducted."
        ),
        "related_form": [],
        "source_url": "https://www.epfo.gov.in/faq-epfo/",
    },
    {
        "faq_number": 8,
        "category": "Claim & withdrawals",
        "question": "Can a member pay contribution in excess of the statutory rate of 12%?",
        "answer": (
            "Yes. The member can pay voluntary contribution in excess of his normal "
            "contribution of 12% of Rs.15000/-. The total contribution i.e., voluntary + "
            "mandatory can be up to Rs.15000/- per month. The employer may restrict his own "
            "share to the statutory rate. The member can also contribute on higher wages "
            "i.e., >15000/- after getting permission from APFC/RPFC as per the provisions "
            "of para-266 of the Scheme."
        ),
        "related_form": [],
        "source_url": "https://www.epfo.gov.in/faq-epfo/",
    },
    {
        "faq_number": 9,
        "category": "Claim & withdrawals",
        "question": "Is there any time limit for withdrawal of Provident Fund dues?",
        "answer": (
            "Only in the case of resignation from service not superannuation a member has "
            "to wait for a period of two months for withdrawal of the PF amount."
        ),
        "related_form": [],
        "source_url": "https://www.epfo.gov.in/faq-epfo/",
    },
    {
        "faq_number": 10,
        "category": "Claim & withdrawals",
        "question": "In case of change in employment whether a member can get his PF account transferred?",
        "answer": (
            "On change in employment, the member should necessarily get his PF account "
            "transferred to his present establishment, duly submitting Form 13R. A member "
            "can submit claim for transfer online using member interface at unified portal."
        ),
        "related_form": ["Form 13R"],
        "source_url": "https://www.epfo.gov.in/faq-epfo/",
    },
    {
        "faq_number": 11,
        "category": "Claim & withdrawals",
        "question": "If past accumulations are not transferred on cancellation of exemption, how the provident fund amount is paid to the members?",
        "answer": (
            "The local RPFC will ensure transfer of securities/cash and arrange for refund "
            "of dues to the members."
        ),
        "related_form": [],
        "source_url": "https://www.epfo.gov.in/faq-epfo/",
    },
    {
        "faq_number": 12,
        "category": "Claim & withdrawals",
        "question": "How is a PF member informed of the transfer affected?",
        "answer": (
            "A copy of Transfer Certificate Annexure-K issued to the transferee Regional "
            "P.F. Commissioner/P.F. Trust giving full details of the transfer can be "
            "requested from the EPF office."
        ),
        "related_form": ["Annexure-K"],
        "source_url": "https://www.epfo.gov.in/faq-epfo/",
    },
    {
        "faq_number": 13,
        "category": "Claim & withdrawals",
        "question": "If an employee is not given the PF membership, to whom he can approach?",
        "answer": (
            "He can approach his employer failing which he can approach the Regional "
            "Provident Fund Commissioner of the nearest PF office."
        ),
        "related_form": [],
        "source_url": "https://www.epfo.gov.in/faq-epfo/",
    },
    {
        "faq_number": 14,
        "category": "Claim & withdrawals",
        "question": "Can an employee become a member of EPF without any age restriction?",
        "answer": (
            "There is no age restriction for becoming a member of the Provident Fund, "
            "whereas an employee who has already attained the age of 58 cannot become "
            "a member of the Pension Fund."
        ),
        "related_form": [],
        "source_url": "https://www.epfo.gov.in/faq-epfo/",
    },
    {
        "faq_number": 15,
        "category": "Claim & withdrawals",
        "question": "Whether an employee can become a member of the EPF without any restriction to his salary/wages?",
        "answer": (
            "The employees who are drawing the basic wages and dearness allowance up to "
            "Rs.15, 000/- are alone eligible to become a member. He will continue to be a "
            "member even when his pay exceeds Rs.15, 000/-. However, his contribution to "
            "the Fund will be restricted to Rs.15, 000/-. The employer is also required to "
            "pay his matching contribution up to Rs.15, 000/-. Employees drawing more than "
            "Rs.15000/- can also become a member of EPF by giving option under para 266 of "
            "the EPF Scheme. The option has to be submitted to the EPF office within 6 months "
            "of joining of such member."
        ),
        "related_form": [],
        "source_url": "https://www.epfo.gov.in/faq-epfo/",
    },
    {
        "faq_number": 16,
        "category": "Claim & withdrawals",
        "question": "Whether an apprentice can become a member of the EPF?",
        "answer": "No. But when he ceases to be an apprentice he should be enrolled immediately.",
        "related_form": [],
        "source_url": "https://www.epfo.gov.in/faq-epfo/",
    },
    {
        "faq_number": 17,
        "category": "Claim & withdrawals",
        "question": "If an employee is drawing more than Rs. 15000/- Basic + DA only is he required to become a member of the EPF?",
        "answer": (
            "Such employee is not required to become a member, if he is not already holding "
            "the PF membership. Otherwise, if both the employer and employee are willing, "
            "he can become a member by giving option under Para-26 6 of the PF Scheme. "
            "The option has to be submitted to the EPF office within 6 months of joining "
            "of such member."
        ),
        "related_form": [],
        "source_url": "https://www.epfo.gov.in/faq-epfo/",
    },
    {
        "faq_number": 18,
        "category": "Claim & withdrawals",
        "question": "Whether an employee can continue as a PF member even after his retirement?",
        "answer": "Yes. If one continues to work even after attaining the superannuation age.",
        "related_form": [],
        "source_url": "https://www.epfo.gov.in/faq-epfo/",
    },
    {
        "faq_number": 19,
        "category": "Claim & withdrawals",
        "question": "Is there any option available to an employee whether to become a member of the EPF or not?",
        "answer": "No option.",
        "related_form": [],
        "source_url": "https://www.epfo.gov.in/faq-epfo/",
    },
    {
        "faq_number": 20,
        "category": "Claim & withdrawals",
        "question": "Whether an EPF member can discontinue his membership, while in employment?",
        "answer": "Not permissible.",
        "related_form": [],
        "source_url": "https://www.epfo.gov.in/faq-epfo/",
    },
]
