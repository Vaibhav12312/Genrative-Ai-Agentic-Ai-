
"""Deterministic PF withdrawal rule calculator.

This module intentionally uses only Python's standard-library datetime module.
It provides rule calculations, not a legal/tax determination.
"""
from datetime import date
from typing import Any


def _parse_date(value: str | date, field_name: str) -> date:
    if isinstance(value, date):
        return value
    try:
        return date.fromisoformat(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be an ISO date (YYYY-MM-DD)") from None


def _add_months(day: date, months: int) -> date:
    """Add calendar months, clamping the day to the target month's last day."""
    month_index = day.month - 1 + months
    year = day.year + month_index // 12
    month = month_index % 12 + 1
    # First day of next month minus one day gives the target month's last day.
    if month == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month + 1, 1)
    last_day = (next_month - date.resolution).day
    return date(year, month, min(day.day, last_day))


def _completed_years(start: date, end: date) -> int:
    years = end.year - start.year
    if (end.month, end.day) < (start.month, start.day):
        years -= 1
    return years


def pf_withdrawal_checker(
    join_date: str | date,
    exit_date: str | date,
    age: int,
    resignation: bool = True,
) -> dict[str, Any]:
    """Calculate the requested PF withdrawal dates and rule flags.

    Rule assumptions encoded for this task:
    * On resignation, earliest final withdrawal is exit date + 2 calendar months.
    * TDS may apply when completed service is below 5 years.
    * A scheme certificate is mandatory when service is at least 10 years
      and the member is below 58 years old.
    """
    joined = _parse_date(join_date, "join_date")
    exited = _parse_date(exit_date, "exit_date")
    if exited < joined:
        raise ValueError("exit_date cannot be earlier than join_date")
    if not isinstance(age, int) or isinstance(age, bool) or not 0 <= age <= 120:
        raise ValueError("age must be an integer between 0 and 120")
    if not isinstance(resignation, bool):
        raise ValueError("resignation must be a boolean")

    service_years = _completed_years(joined, exited)
    earliest = _add_months(exited, 2) if resignation else exited

    return {
        "join_date": joined.isoformat(),
        "exit_date": exited.isoformat(),
        "age": age,
        "completed_service_years": service_years,
        "earliest_final_withdrawal_date": earliest.isoformat(),
        "tds_can_apply": service_years < 5,
        "scheme_certificate_mandatory": service_years >= 10 and age < 58,
        "rule_notes": [
            "The two-month waiting period is applied only when resignation is true.",
            "TDS flag is based on completed service being under five years.",
            "Scheme-certificate flag is based on at least ten years of service and age below 58.",
        ],
    }
