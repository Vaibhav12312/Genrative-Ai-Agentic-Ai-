# EPFOSathi Checkpoint 2 — live demo script

Estimated walkthrough: 3–5 minutes.

## Start

On Windows, double-click `START_DEMO.bat`, or run:

```powershell
python -m pip install -r requirements.txt
python run_demo.py
```

Open http://localhost:8501/?demo=1. The mock API health endpoint is http://localhost:8000/health.

## Walkthrough

| # | Action | Expected result |
|---|---|---|
| 1 | Show the Streamlit page and sidebar | EPFOSathi chat, backend URL, `ask` / `agent` route selector |
| 2 | Ask `When can I withdraw my PF after leaving my job?` | Mock answer and expandable Sources / citations |
| 3 | Switch to `agent`; ask `Is TDS applicable for me?` | Agent route response with citation |
| 4 | Click 👍 on one answer and 👎 on another | Feedback saved message; each answer's buttons lock after voting |
| 5 | Show the PF date fields in demo mode | Joining 01 Jan 2020 and exit 10 Mar 2024 |
| 6 | Show My PF timeline | Can withdraw from 10 May 2024; 5-year TDS line 01 Jan 2025; Scheme certificate (10 years) 01 Jan 2030 |
| 7 | Untick `I have left this employment` and rebuild | Withdrawal marker disappears; joining-based markers remain |
| 8 | Optional: stop mock backend and ask another question | Friendly backend connection error |

## Capture live screenshot

Install Playwright and its browser once:

```powershell
python -m pip install -r requirements-capture.txt
python -m playwright install chromium
```

Keep the Streamlit demo running, then in a second terminal:

```powershell
python scripts/capture_screenshot.py
```

The script saves `screenshots/checkpoint-2-live.png`. This is the genuine browser screenshot to include in the final README; the `*-preview.png` images are static previews only.

## Optional screen recording

On Windows, use `Windows + Alt + R` to start/stop Xbox Game Bar recording. Save the resulting video from `Videos\Captures` alongside your submission if video evidence is requested.

## Stop

Return to the terminal running `python run_demo.py` and press `Ctrl+C`.

> Demo backend responses are canned examples for UI demonstration, not live EPFO advice or an official eligibility decision.
