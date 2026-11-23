"""Deterministic date rules. The LLM never computes these; it only explains the result.

Rule parameters come from the FAQ text and are flagged for verification against the
current official EPFO guidance (see PROGRESS.md).
"""
from __future__ import annotations

import calendar
from datetime import date

INOPERATIVE_AFTER_MONTHS = 36   # FAQ 1: account inoperative 36 months after retirement at/after 55
RETIREMENT_AGE_FLOOR = 55
WITHDRAWAL_WAIT_MONTHS = 2      # FAQ 9 (sample): resignation -> wait before PF withdrawal
OPTION_WINDOW_MONTHS = 6        # FAQ 15/17: para 26(6) option within 6 months of joining


def add_months(start: date, months: int) -> date:
    """Add calendar months; clamp the day (e.g. 31 Aug + 6 -> 28/29 Feb)."""
    idx = start.month - 1 + months
    year, month = start.year + idx // 12, idx % 12 + 1
    day = min(start.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def age_on(dob: date, on: date) -> int:
    return on.year - dob.year - ((on.month, on.day) < (dob.month, dob.day))


def inoperative_date(retirement: date, dob: date) -> dict:
    age = age_on(dob, retirement)
    if age < RETIREMENT_AGE_FLOOR:
        # FAQ 1: early retirees still earn interest until age 58 per the FAQ wording.
        age58 = add_months(dob, 58 * 12)
        return {"rule": "retired_before_55", "interest_until": age58.isoformat(),
                "age_at_retirement": age, "verify": True}
    cutoff = add_months(retirement, INOPERATIVE_AFTER_MONTHS)
    return {"rule": "retired_at_or_after_55", "interest_until": cutoff.isoformat(),
            "age_at_retirement": age, "verify": True}


def withdrawal_eligible_on(separation: date, months: int = WITHDRAWAL_WAIT_MONTHS) -> str:
    return add_months(separation, months).isoformat()


def option_deadline(joining: date) -> str:
    return add_months(joining, OPTION_WINDOW_MONTHS).isoformat()


def is_eligible_today(separation: date, today: date, months: int = WITHDRAWAL_WAIT_MONTHS) -> bool:
    return today >= add_months(separation, months)
