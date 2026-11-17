"""Visual horizontal "My PF timeline" as self-contained HTML/CSS.

Pure function, independent of Streamlit, so it can be unit-tested and rendered in any browser.
Colours use translucent greys / currentColor so it reads on both light and dark Streamlit themes.
"""
from __future__ import annotations

import html
from datetime import date
from typing import Optional, Sequence

try:
    from pf_timeline import TimelineMarker
except ImportError:  # pragma: no cover
    from ui.pf_timeline import TimelineMarker

# Colour per required marker key; reference points (joined / exited / today) are neutral.
MARKER_COLOURS = {"withdrawal": "#2e8b57", "tds": "#d9822b", "scheme": "#5b5fd6"}
AXIS_TOP = 150          # px, vertical position of the axis line inside the widget
HEIGHT = 270


def _fmt(day: date) -> str:
    return day.strftime("%d %b %Y")


def _position(day: date, lo: date, hi: date) -> float:
    """Percent position along the axis, with a 4% margin each side."""
    span = (hi - lo).days
    if span <= 0:
        return 50.0
    return 4.0 + 92.0 * (day - lo).days / span


def _align(pct: float) -> str:
    if pct < 15:
        return "0"
    if pct > 85:
        return "-100%"
    return "-50%"


def _point(pct: float, colour: str, above: bool, level: int, title: str, when: date, sub: str, hollow: bool = False, align: str = "") -> str:
    if above:
        stem = 24 + level * 60
        stem_top, label_top = AXIS_TOP - stem, AXIS_TOP - stem - 52
    else:
        stem = 24 + level * 44
        stem_top, label_top = AXIS_TOP, AXIS_TOP + stem
    fill = "transparent" if hollow else colour
    align = align or _align(pct)
    return (
        f'<div style="position:absolute;left:{pct:.2f}%;top:{stem_top}px;height:{stem}px;border-left:2px solid {colour};opacity:.55"></div>'
        f'<div style="position:absolute;left:{pct:.2f}%;top:{AXIS_TOP - 7}px;width:14px;height:14px;margin-left:-7px;'
        f'border-radius:50%;background:{fill};border:3px solid {colour};box-sizing:border-box"></div>'
        f'<div style="position:absolute;left:{pct:.2f}%;top:{label_top}px;transform:translateX({align});'
        f'white-space:nowrap;font-size:12.5px;line-height:1.3;{"text-align:right;" if align == "-100%" else ""}">'
        f'<b style="color:{colour}">{html.escape(title)}</b><br>{_fmt(when)}<br>'
        f'<span style="opacity:.7;font-size:11.5px">{html.escape(sub)}</span></div>'
    )


def timeline_html(
    joining: date,
    exit_day: Optional[date],
    markers: Sequence[TimelineMarker],
    today: Optional[date] = None,
) -> str:
    """Return an HTML string drawing joining / exit / today and the required milestone markers on one axis."""
    today = today or date.today()
    refs: list[tuple[str, date, str]] = [("Joined", joining, "your joining date")]
    if exit_day:
        refs.append(("Exited", exit_day, "your exit date"))
    refs.append(("Today", today, "as of now"))

    all_days = [joining, today] + ([exit_day] if exit_day else []) + [m.when for m in markers]
    lo, hi = min(all_days), max(all_days)

    parts = [
        f'<div class="pf-timeline" style="position:relative;width:100%;height:{HEIGHT}px;margin:6px 0 10px">',
        f'<div style="position:absolute;left:0;right:0;top:{AXIS_TOP - 2}px;height:4px;border-radius:2px;background:rgba(128,128,128,.35)"></div>',
    ]
    # Required milestone markers above the axis, alternating heights so neighbouring labels do not collide.
    ordered = sorted(markers, key=lambda x: (x.when, x.key))
    pcts = [_position(m.when, lo, hi) for m in ordered]
    for i, m in enumerate(ordered):
        align = ""
        if i % 2 == 0:  # short label: steer away from a nearby taller stem so the stem never crosses its text
            tall = [pcts[j] for j in range(len(ordered)) if j % 2 == 1]
            if any(0 <= t - pcts[i] < 20 for t in tall):
                align = "-100%"
            elif any(0 < pcts[i] - t < 20 for t in tall):
                align = "0"
        status = "reached" if m.when <= today else "upcoming"
        parts.append(_point(pcts[i], MARKER_COLOURS.get(m.key, "#888"), True, i % 2, m.label, m.when, status, align=align))
    # Reference points below the axis.
    for i, (title, day, sub) in enumerate(refs):
        colour = "#c0392b" if title == "Today" else "#7f8c8d"
        parts.append(_point(_position(day, lo, hi), colour, False, i % 2, title, day, sub, hollow=True))
    parts.append("</div>")
    return "".join(parts)
