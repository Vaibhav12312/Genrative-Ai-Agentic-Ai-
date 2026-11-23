from datetime import date

from app.services import datetools as d
from app.services.dedupe import dedupe, is_outdated, similarity


def rec(q, a, url="https://www.epfindia.gov.in/site_en/FAQ.php", **kw):
    return {"question": q, "answer": a, "source_url": url, **kw}


def test_near_duplicates_merge_and_keep_newest():
    old = rec("How can I transfer my PF account?", "Use Form 13.", updated_on="2019-01-01")
    new = rec("How can I transfer my PF account", "Use Form 13R online.", updated_on="2024-05-01")
    out, _ = dedupe([old, new])
    assert len(out) == 1 and "13R" in out[0]["answer"]
    assert out[0]["alternatives"]


def test_different_questions_stay_separate():
    out, _ = dedupe([rec("What is UAN?", "x"), rec("How to withdraw PF?", "y")])
    assert len(out) == 2


def test_outdated_form_and_url_flagged():
    assert is_outdated(rec("q", "Submit Form 19", ))
    assert not is_outdated(rec("q", "Submit the Composite Claim Form instead of Form 19"))
    assert is_outdated(rec("q", "a", url="https://www.epfindia.com/old"))


def test_undated_conflict_goes_to_review():
    _, review = dedupe([rec("Is PF taxable?", "Yes."), rec("Is PF taxable", "No.")])
    assert review


def test_similarity_ignores_punctuation_case():
    assert similarity("What is UAN?", "what is uan") == 1.0


def test_add_months_clamps_month_end():
    assert d.add_months(date(2024, 8, 31), 6) == date(2025, 2, 28)
    assert d.add_months(date(2023, 8, 31), 6) == date(2024, 2, 29)


def test_inoperative_after_retirement_at_58():
    r = d.inoperative_date(date(2026, 3, 1), date(1968, 3, 1))
    assert r["interest_until"] == "2029-03-01" and r["age_at_retirement"] == 58


def test_withdrawal_wait():
    assert d.withdrawal_eligible_on(date(2026, 1, 31)) == "2026-03-31"
    assert d.is_eligible_today(date(2026, 1, 1), date(2026, 3, 1))
    assert not d.is_eligible_today(date(2026, 1, 1), date(2026, 2, 28))


def test_option_deadline():
    assert d.option_deadline(date(2026, 8, 31)) == "2027-02-28"

def test_all_three_configured_date_intervals_and_boundaries():
    # 36-month inoperative-interest calculation from retirement at/after age 55.
    result = d.inoperative_date(date(2026, 11, 23), date(1968, 11, 23))
    assert result["interest_until"] == "2029-11-23"
    assert result["verify"] is True  # policy value still requires official verification

    # Two calendar months after separation; the day is clamped at month end.
    assert d.withdrawal_eligible_on(date(2026, 12, 31)) == "2027-02-28"
    assert d.is_eligible_today(date(2026, 12, 31), date(2027, 2, 28))
    assert not d.is_eligible_today(date(2026, 12, 31), date(2027, 2, 27))

    # Six calendar months from joining; leap-year/month-end behavior is explicit.
    assert d.option_deadline(date(2024, 8, 31)) == "2025-02-28"
    assert d.option_deadline(date(2023, 8, 31)) == "2024-02-29"

