
import pytest
from app.tools import pf_withdrawal_checker


def test_two_month_waiting_period():
    result = pf_withdrawal_checker("2020-01-01", "2024-01-15", 30, True)
    assert result["earliest_final_withdrawal_date"] == "2024-03-15"


def test_month_end_clamps_correctly():
    result = pf_withdrawal_checker("2020-01-01", "2024-12-31", 30, True)
    assert result["earliest_final_withdrawal_date"] == "2025-02-28"


def test_no_resignation_no_wait():
    result = pf_withdrawal_checker("2020-01-01", "2024-01-15", 30, False)
    assert result["earliest_final_withdrawal_date"] == "2024-01-15"


def test_tds_under_five_completed_years():
    assert pf_withdrawal_checker("2020-06-01", "2025-05-31", 30)["tds_can_apply"] is True
    assert pf_withdrawal_checker("2020-06-01", "2025-06-01", 30)["tds_can_apply"] is False


def test_scheme_certificate_threshold():
    assert pf_withdrawal_checker("2010-01-01", "2020-01-01", 57)["scheme_certificate_mandatory"] is True
    assert pf_withdrawal_checker("2010-01-01", "2020-01-01", 58)["scheme_certificate_mandatory"] is False
    assert pf_withdrawal_checker("2010-01-01", "2019-12-31", 57)["scheme_certificate_mandatory"] is False


@pytest.mark.parametrize("args", [
    ("2025-01-01", "2024-01-01", 30),
    ("bad-date", "2024-01-01", 30),
    ("2020-01-01", "2024-01-01", -1),
])
def test_invalid_inputs(args):
    with pytest.raises(ValueError):
        pf_withdrawal_checker(*args)
