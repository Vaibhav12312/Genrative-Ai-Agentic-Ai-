"""Render screenshots/checkpoint-2-preview.png WITHOUT Streamlit.

Uses the app's real build_pf_timeline() and the mock backend's real answer, laid out in
static HTML and captured with Playwright. It is a rendered preview, not the live app.
Use scripts/capture_screenshot.py for a true capture of the running Streamlit UI.
"""
from __future__ import annotations

import html
import sys
import shutil
from PIL import Image
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "ui"), str(ROOT / "mock_backend")]
from pf_timeline import build_pf_timeline  # noqa: E402
from timeline_view import timeline_html  # noqa: E402
from server import answer_for  # noqa: E402
from playwright.sync_api import sync_playwright  # noqa: E402

Q = "When can I withdraw my PF after leaving my job?"
JOIN, EXIT = date(2020, 1, 1), date(2024, 3, 10)
res = answer_for(Q, "ask")
marks = build_pf_timeline(JOIN, EXIT)
e = html.escape

cards = "".join(
    f'<div class="m"><b>{e(m.label)}</b><div class="d">{m.when.strftime("%d %b %Y")}</div>'
    f'<small>{e(m.detail[:95])}…</small></div>' for m in marks)
steps = " &rarr; ".join(f"<b>{e(m.label)}</b> &middot; {m.when.strftime('%d %b %Y')}" for m in marks)
cites = "".join(f'<li><a>{e(c["title"])}</a> &middot; {e(c["url"])}</li>' for c in res["citations"])

page = f"""<html><body style="margin:0;font-family:DejaVu Sans,Arial,sans-serif;background:#f6f7fb;color:#16213e">
<style>
.wrap{{display:flex;gap:18px;padding:18px}} .card{{background:#fff;border:1px solid #dde2ee;border-radius:14px;padding:20px}}
.m{{border:1px solid #dde2ee;border-radius:10px;padding:12px;margin:10px 0;background:#f8f9fc}} .d{{font-size:24px;font-weight:700;margin:4px 0}}
small{{color:#667}} .u{{background:#eef3ff;border-radius:10px;padding:12px;margin:10px 0 }} .a{{background:#f1f4ff;border-radius:10px;padding:14px;margin:12px 0}}
.btn{{display:inline-block;border:1px solid #ccd;border-radius:8px;padding:4px 14px;margin-right:8px}} .in{{border:1px solid #dde;border-radius:10px;padding:12px;color:#889;margin-top:30px}}
</style>
<div style="padding:14px 22px"><h2 style="margin:0">EPFOSathi</h2><small>Your provident-fund companion &middot; Ask questions, inspect sources, and map key PF milestones.</small></div>
<div class="wrap">
 <div class="card" style="flex:1.35"><h3>Ask EPFOSathi</h3>
  <div class="u"><b>You:</b> {e(Q)}</div>
  <div class="a"><b>EPFOSathi:</b><br>{e(res["answer"])}</div>
  <b>Sources / citations</b><ul>{cites}</ul>
  <div><span class="btn">[ up ] Helpful</span><span class="btn">[ down ] Not helpful</span></div>
  <div class="in">Ask about EPF, EPS, withdrawals, transfers, or tax...</div></div>
 <div class="card" style="flex:1"><h3>PF dates</h3>
  <small>Date of joining</small> <b>{JOIN:%d %b %Y}</b> &nbsp; <small>Date of exit</small> <b>{EXIT:%d %b %Y}</b>
  <h3>My PF timeline</h3>{timeline_html(JOIN, EXIT, marks, date.today())}{cards}
  <small style="color:#9a6700">Dates are estimates - verify current EPFO / tax rules.</small></div>
</div>
<div style="text-align:center;font-size:12px;color:#889;padding-bottom:8px">Rendered preview (static HTML using the app's real timeline code and mock-backend data) - not a capture of the running Streamlit app.</div>
</body></html>"""

out = ROOT / "screenshots" / "checkpoint-2-preview.png"
with sync_playwright() as p:
    chromium = shutil.which("chromium") or shutil.which("chromium-browser")
    launch_options = {"headless": True}
    if chromium:
        launch_options["executable_path"] = chromium
        launch_options["args"] = ["--no-sandbox"]
    b = p.chromium.launch(**launch_options); pg = b.new_page(viewport={"width": 1400, "height": 860}, device_scale_factor=1)
    pg.set_content(page); pg.screenshot(path=str(out), full_page=True); b.close()
print("Saved", out)
# Produce focused evidence panels from the same browser-rendered preview.
shot = Image.open(out)
shot.crop((12, 78, 795, shot.height - 28)).save(ROOT / "screenshots" / "checkpoint-2-chat-demo.png")
shot.crop((795, 78, shot.width - 10, shot.height - 28)).save(ROOT / "screenshots" / "checkpoint-2-timeline-demo.png")
print("Saved focused chat and timeline demo panels")
