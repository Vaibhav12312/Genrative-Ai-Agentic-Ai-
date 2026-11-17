"""One-command live demo: starts the mock backend and the Streamlit UI together.

    python run_demo.py                 # mock backend on :8000 + UI on :8501
    python run_demo.py --no-mock       # UI only (use your real API; set EPFOSATHI_API_URL)
Press Ctrl+C to stop everything.
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
import socket
import webbrowser
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-mock", action="store_true", help="do not start the mock backend")
    ap.add_argument("--port", default="8501", help="Streamlit port")
    ap.add_argument("--open-browser", action="store_true", help="open the local demo after Streamlit starts")
    args = ap.parse_args()
    try:
        import streamlit  # noqa: F401
    except ImportError:
        print("Streamlit is not installed. Run: pip install -r requirements.txt")
        return 1
    procs = []
    try:
        if not args.no_mock:
            procs.append(subprocess.Popen([sys.executable, str(ROOT / "mock_backend" / "server.py")]))
            # Wait until the local mock API is accepting connections before opening Streamlit.
            deadline = time.monotonic() + 10
            while time.monotonic() < deadline:
                if procs[0].poll() is not None:
                    raise RuntimeError("Mock backend exited before it became ready. Check whether port 8000 is already in use.")
                try:
                    with socket.create_connection(("127.0.0.1", 8000), timeout=0.25):
                        break
                except OSError:
                    time.sleep(0.2)
            else:
                raise RuntimeError("Mock backend did not become ready on port 8000.")
            os.environ.setdefault("EPFOSATHI_API_URL", "http://localhost:8000")
        procs.append(subprocess.Popen([sys.executable, "-m", "streamlit", "run", str(ROOT / "ui" / "app.py"),
                                       "--server.port", args.port]))
        demo_url = f"http://localhost:{args.port}/?demo=1"
        print(f"\nLive demo: {demo_url}   (Ctrl+C to stop)\n")
        if args.open_browser:
            deadline = time.monotonic() + 30
            while time.monotonic() < deadline:
                if procs[-1].poll() is not None:
                    raise RuntimeError("Streamlit exited before it became ready.")
                try:
                    with socket.create_connection(("127.0.0.1", int(args.port)), timeout=0.25):
                        webbrowser.open(demo_url)
                        break
                except OSError:
                    time.sleep(0.25)
            else:
                print("Streamlit is taking longer than expected; open the URL above manually.")
        procs[-1].wait()
    except KeyboardInterrupt:
        pass
    finally:
        for p in procs:
            p.terminate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
