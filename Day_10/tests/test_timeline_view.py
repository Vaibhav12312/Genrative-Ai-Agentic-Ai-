import sys
from datetime import date
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "ui"))
from pf_timeline import build_pf_timeline
from timeline_view import timeline_html, _position

JOIN, EXIT, TODAY = date(2020, 1, 1), date(2024, 3, 10), date(2026, 11, 17)


def test_all_three_required_markers_are_drawn_with_dates():
    out = timeline_html(JOIN, EXIT, build_pf_timeline(JOIN, EXIT), TODAY)
    for label in ("Can withdraw from", "5-year TDS line", "Scheme certificate (10 years)"):
        assert label in out
    for text in ("10 May 2024", "01 Jan 2025", "01 Jan 2030"):
        assert text in out


def test_joining_only_mode_has_no_withdraw_marker_or_exit_point():
    out = timeline_html(JOIN, None, build_pf_timeline(JOIN), TODAY)
    assert "Can withdraw from" not in out and "Exited" not in out
    assert "5-year TDS line" in out and "Scheme certificate (10 years)" in out


def test_reached_vs_upcoming_status_uses_today():
    out = timeline_html(JOIN, EXIT, build_pf_timeline(JOIN, EXIT), TODAY)
    assert out.count("reached") == 2 and out.count("upcoming") == 1  # withdraw + TDS reached, scheme upcoming


def test_positions_are_ordered_and_within_axis():
    lo, hi = JOIN, date(2030, 1, 1)
    assert _position(lo, lo, hi) == 4.0 and _position(hi, lo, hi) == 96.0
    assert _position(EXIT, lo, hi) < _position(TODAY, lo, hi)


def test_degenerate_range_does_not_divide_by_zero():
    assert _position(JOIN, JOIN, JOIN) == 50.0
