import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ui"))
from pf_timeline import add_months, add_years, build_pf_timeline


def test_exit_withdrawal_marker_and_order():
    markers = build_pf_timeline(date(2020, 1, 15), date(2024, 3, 10))
    by_key = {m.key: m for m in markers}
    assert by_key["withdrawal"].when == date(2024, 5, 10)
    assert by_key["tds"].when == date(2025, 1, 15)
    assert by_key["scheme"].when == date(2030, 1, 15)
    assert markers == sorted(markers, key=lambda m: (m.when, m.key))


def test_no_exit_still_has_tax_and_scheme_markers():
    markers = build_pf_timeline(date(2021, 6, 1))
    assert [m.key for m in markers] == ["tds", "scheme"]


def test_leap_day_year_clamps_to_february_28():
    assert add_years(date(2020, 2, 29), 5) == date(2025, 2, 28)


def test_month_end_clamps_to_target_month():
    assert add_months(date(2024, 1, 31), 1) == date(2024, 2, 29)


def test_exit_before_joining_is_rejected():
    try:
        build_pf_timeline(date(2024, 2, 1), date(2024, 1, 31))
    except ValueError as exc:
        assert "earlier" in str(exc)
    else:
        raise AssertionError("Expected ValueError")
