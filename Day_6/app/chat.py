"""Chat logic: build prompts -> call LLM -> parse/validate the JSON reply."""
import json
import re

from app import llm
from app.prompts import build_user_prompt, load_system_prompt
from app.schemas import ChatResponse


def _extract_json(raw: str) -> dict:
    """Parse JSON even if the model wrapped it in ```fences``` or added chatter."""
    text = raw.strip()
    text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, flags=re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise


def parse_reply(raw: str) -> tuple[ChatResponse, bool]:
    """Return (response, parsed_ok). Never raises: falls back to a safe response."""
    try:
        data = _extract_json(raw)
        conf = float(data.get("confidence", 0.0))
        return (
            ChatResponse(
                answer=str(data["answer"]).strip(),
                confidence=min(max(conf, 0.0), 1.0),
                follow_up=str(data.get("follow_up", "")).strip(),
            ),
            True,
        )
    except Exception:
        return (
            ChatResponse(
                answer=raw.strip() or "Sorry, I could not produce an answer.",
                confidence=0.0,
                follow_up="Could you rephrase your question?",
            ),
            False,
        )


def run_chat(message: str, version: str = "v2") -> tuple[ChatResponse, bool]:
    raw = llm.generate(load_system_prompt(), build_user_prompt(message, version))
    return parse_reply(raw)
