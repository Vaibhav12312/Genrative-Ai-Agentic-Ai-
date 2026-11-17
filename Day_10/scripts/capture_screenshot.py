"""Capture genuine browser evidence from a running EPFOSathi Streamlit app.

Start the demo first with `python run_demo.py`, then run:
    python scripts/capture_screenshot.py
Optional URL:
    python scripts/capture_screenshot.py http://localhost:8501

The script opens the app in demo mode (sample dates), asks a PF question,
expands citations when available, and saves screenshots/checkpoint-2-live.png.
Requires: `pip install playwright` and `playwright install chromium`.
"""
from __future__ import annotations

import sys
from pathlib import Path
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8501"
URL = BASE_URL.rstrip("/") + "/?demo=1"
OUT = ROOT / "screenshots" / "checkpoint-2-live.png"
QUESTION = "When can I withdraw my PF after leaving my job?"


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1600, "height": 1100}, device_scale_factor=1)
        try:
            page.goto(URL, wait_until="domcontentloaded", timeout=30000)
            page.get_by_text("EPFOSathi", exact=False).first.wait_for(timeout=30000)
            # Demo mode preselects the exit date and the three timeline milestones.
            page.get_by_text("Scheme certificate (10 years)", exact=False).wait_for(timeout=15000)
            chat = page.get_by_role("textbox", name="Ask about EPF, EPS, withdrawals, transfers, or tax…")
            chat.fill(QUESTION)
            chat.press("Enter")
            page.get_by_text("A final EPF settlement can generally", exact=False).wait_for(timeout=30000)
            try:
                page.get_by_text("Sources / citations", exact=True).first.wait_for(timeout=10000)
            except PlaywrightTimeoutError:
                pass
            # Expand a collapsed citation section if present.
            citations = page.get_by_text("Sources / citations", exact=True).last
            if citations.count():
                try:
                    citations.click(timeout=1500)
                except Exception:
                    pass
            page.wait_for_timeout(1200)
            page.screenshot(path=str(OUT), full_page=True)
            print(f"Live Streamlit screenshot saved: {OUT}")
            return 0
        except Exception as exc:
            print(f"Could not capture the live app at {URL}: {exc}")
            print("Start it first with `python run_demo.py`, then retry this command.")
            return 1
        finally:
            browser.close()


if __name__ == "__main__":
    raise SystemExit(main())
