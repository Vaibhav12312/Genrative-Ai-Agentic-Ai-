"""Tiny stdlib stand-in for the EPFOSathi API, for demos and UI testing.

Run:  python mock_backend/server.py            (listens on http://localhost:8000)
Routes: POST /ask, POST /agent  ->  {"answer": ..., "citations": [...]}
This is NOT the real EPFOSathi backend; answers are canned and indicative only.
"""
from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

EPFO = {"title": "EPFO official portal", "url": "https://www.epfindia.gov.in"}
UNIFIED = {"title": "EPFO Member Services (Unified Portal)", "url": "https://unifiedportal-mem.epfindia.gov.in"}

TOPICS = [
    (("withdraw", "settlement", "claim"),
     "A final EPF settlement can generally be claimed two months after you leave employment, subject to "
     "current EPFO rules, an active UAN and completed KYC.", [EPFO, UNIFIED]),
    (("tds", "tax"),
     "TDS on EPF withdrawal generally applies when continuous service is under five years; "
     "transferred service from earlier employers can count towards the five years.", [EPFO]),
    (("scheme certificate", "pension", "eps", "10 year", "ten year"),
     "With ten years of eligible EPS service you may qualify for a monthly pension; a Scheme Certificate "
     "can preserve your pensionable service if you exit earlier.", [EPFO]),
    (("transfer",),
     "EPF transfer between employers is done online through the member portal using your UAN (Form 13).", [UNIFIED]),
]
FALLBACK = ("I can help with EPF, EPS, withdrawals, transfers and tax. Try asking when you can withdraw "
            "after leaving a job.", [EPFO])


def answer_for(question: str, route: str) -> dict:
    q = (question or "").lower()
    text, cites = next(((t, c) for keys, t, c in TOPICS if any(k in q for k in keys)), FALLBACK)
    if route == "agent":
        text = "[agent] " + text
    return {"answer": text, "citations": cites}


class Handler(BaseHTTPRequestHandler):
    def _send(self, code: int, body: dict) -> None:
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):  # noqa: N802
        if self.path.rstrip("/") == "/health":
            return self._send(200, {"status": "ok", "service": "EPFOSathi mock backend"})
        return self._send(404, {"error": "not found"})

    def do_POST(self):  # noqa: N802
        route = self.path.strip("/")
        if route not in ("ask", "agent"):
            return self._send(404, {"error": "unknown route"})
        try:
            length = int(self.headers.get("Content-Length", 0))
            payload = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            return self._send(400, {"error": "invalid JSON"})
        question = payload.get("question") or payload.get("query") or payload.get("message") or ""
        if not str(question).strip():
            return self._send(422, {"error": "question is required"})
        self._send(200, answer_for(str(question), route))

    def log_message(self, *args):  # keep demo console quiet
        pass


if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    print(f"Mock EPFOSathi API on http://localhost:{port}  (POST /ask, POST /agent)")
    ThreadingHTTPServer(("127.0.0.1", port), Handler).serve_forever()
