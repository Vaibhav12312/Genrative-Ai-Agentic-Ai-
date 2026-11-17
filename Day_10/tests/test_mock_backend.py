import json
import sys
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "ui"))
sys.path.insert(0, str(ROOT / "mock_backend"))
from server import Handler, answer_for  # noqa: E402
from api_client import call_backend  # noqa: E402


def _serve():
    srv = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def test_answer_for_routes_and_citations():
    assert answer_for("When can I withdraw?", "ask")["citations"]
    assert answer_for("hello", "agent")["answer"].startswith("[agent]")


def test_ui_client_round_trip_against_mock_for_both_routes():
    srv = _serve()
    try:
        base = f"http://127.0.0.1:{srv.server_address[1]}"
        for route in ("ask", "agent"):
            answer, cites = call_backend(base, route, "Is TDS applicable for me?", [])
            assert "TDS" in answer and cites[0]["url"].startswith("https://")
    finally:
        srv.shutdown()


def test_unknown_route_and_empty_question_rejected():
    srv = _serve()
    try:
        base = f"http://127.0.0.1:{srv.server_address[1]}"
        for path, body, code in (("/nope", {"question": "x"}, 404), ("/ask", {}, 422)):
            req = Request(base + path, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
            try:
                urlopen(req)
            except HTTPError as e:
                assert e.code == code
            else:
                raise AssertionError("expected HTTP error")
    finally:
        srv.shutdown()


def test_mock_backend_health_endpoint():
    srv = _serve()
    try:
        with urlopen(f"http://127.0.0.1:{srv.server_address[1]}/health") as response:
            payload = json.loads(response.read())
            assert response.status == 200
            assert payload["status"] == "ok"
    finally:
        srv.shutdown()
