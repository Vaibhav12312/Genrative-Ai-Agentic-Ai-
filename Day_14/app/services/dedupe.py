"""Deduplicate near-identical FAQ records and keep the newest, most authoritative one.

Standard library only. Records are dicts with at least ``question``, ``answer`` and
``source_url``; optional keys: ``updated_on`` (ISO date), ``related_form``.
"""
from __future__ import annotations

import re
from difflib import SequenceMatcher
from typing import Any

SIMILARITY_THRESHOLD = 0.88

# Portal hosts known to be superseded by the Unified Member Portal / new EPFO site.
OUTDATED_URL_MARKERS = (
    "epfindia.gov.in/site_en/index.php",
    "www.epfindia.com",
    "epf.gov.in/mem/",
)
# Forms replaced by the Composite Claim Form (Aadhaar / non-Aadhaar).
SUPERSEDED_FORMS = ("form 19", "form 10c", "form 31")
CURRENT_CLAIM_FORM = "Composite Claim Form"

_STOP = {"the", "a", "an", "is", "are", "of", "to", "in", "for", "can", "i", "he", "she",
         "whether", "if", "or", "and", "any", "his", "her", "member", "employee"}


def normalize(text: str) -> str:
    text = text.casefold()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return " ".join(w for w in text.split() if w not in _STOP)


def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, normalize(a), normalize(b)).ratio()


def is_near_duplicate(a: dict[str, Any], b: dict[str, Any]) -> bool:
    if similarity(a["question"], b["question"]) < SIMILARITY_THRESHOLD:
        return False
    # Same question but materially different answers => keep both for human review.
    return True


def is_outdated(record: dict[str, Any]) -> bool:
    url = str(record.get("source_url", "")).casefold()
    if any(marker in url for marker in OUTDATED_URL_MARKERS):
        return True
    text = f"{record.get('answer', '')} {record.get('related_form') or ''}".casefold()
    return any(form in text for form in SUPERSEDED_FORMS) and "composite" not in text


def _rank(record: dict[str, Any]) -> tuple:
    """Higher is better: not outdated, newest date, longer (more complete) answer."""
    return (
        not is_outdated(record),
        str(record.get("updated_on") or ""),
        len(str(record.get("answer", ""))),
    )


def group_duplicates(records: list[dict[str, Any]]) -> list[list[dict[str, Any]]]:
    groups: list[list[dict[str, Any]]] = []
    for rec in records:
        for group in groups:
            if is_near_duplicate(group[0], rec):
                group.append(rec)
                break
        else:
            groups.append([rec])
    return groups


def dedupe(records: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Return (canonical_records, review_queue).

    Each canonical record gets ``alternatives`` (source URLs of dropped duplicates) and
    ``needs_review`` when the group's answers disagree or no dates were available.
    """
    canonical: list[dict[str, Any]] = []
    review: list[dict[str, Any]] = []
    for group in group_duplicates(records):
        best = max(group, key=_rank)
        out = dict(best)
        out["alternatives"] = [r["source_url"] for r in group if r is not best]
        out["outdated"] = is_outdated(best)
        if len(group) > 1:
            answers = {normalize(str(r["answer"])) for r in group}
            undated = any(not r.get("updated_on") for r in group)
            if len(answers) > 1 and undated:
                out["needs_review"] = True
                review.append({"question": best["question"], "sources": [r["source_url"] for r in group]})
        canonical.append(out)
    return canonical, review
