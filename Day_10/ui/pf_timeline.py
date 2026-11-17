"""Pure PF timeline calculations; kept independent of Streamlit for easy testing."""
from __future__ import annotations

import calendar
from dataclasses import dataclass
from datetime import date
from typing import Optional


def add_months(day: date, months: int) -> date:
    """Add calendar months, clamping the day to the target month's last day."""
    month_index = day.month - 1 + months
    year = day.year + month_index // 12
    month = month_index % 12 + 1
    return date(year, month, min(day.day, calendar.monthrange(year, month)[1]))


def add_years(day: date, years: int) -> date:
    """Add calendar years, mapping Feb 29 to Feb 28 in non-leap years."""
    try:
        return day.replace(year=day.year + years)
    except ValueError:
        return day.replace(year=day.year + years, day=28)


@dataclass(frozen=True)
class TimelineMarker:
    key: str
    label: str
    when: date
    detail: str


def build_pf_timeline(joining_date: date, exit_date: Optional[date] = None) -> list[TimelineMarker]:
    if not isinstance(joining_date, date):
        raise TypeError("joining_date must be a datetime.date")
    if exit_date is not None:
        if not isinstance(exit_date, date):
            raise TypeError("exit_date must be a datetime.date or None")
        if exit_date < joining_date:
            raise ValueError("Exit date cannot be earlier than joining date.")

    markers = []
    if exit_date:
        markers.append(TimelineMarker(
            "withdrawal", "Can withdraw from", add_months(exit_date, 2),
            "Indicative date for final EPF settlement after two months from leaving employment. "
            "Partial withdrawal rules and exceptions may differ. Verify current EPFO rules and your status.",
        ))
    markers.extend([
        TimelineMarker(
            "tds", "5-year TDS line", add_years(joining_date, 5),
            "Five years of continuous recognised EPF service is an important tax threshold. "
            "Previous employer service/transfers can affect the calculation; this date is an estimate.",
        ),
        TimelineMarker(
            "scheme", "Scheme certificate (10 years)", add_years(joining_date, 10),
            "Ten years of eligible EPS/pensionable service is generally the key threshold for pension eligibility. "
            "A Scheme Certificate may preserve pension service in applicable exit situations; it is not an automatic benefit.",
        ),
    ])
    return sorted(markers, key=lambda marker: (marker.when, marker.key))
