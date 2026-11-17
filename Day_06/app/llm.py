"""Provider wrapper: one function, `generate()`, that talks to Groq or Gemini.

The rest of the app never needs to know which provider is active.
Both providers are called over plain HTTPS with httpx (no vendor SDKs).
"""
import httpx

from app.config import get_settings

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"


class LLMError(Exception):
    """Raised for any provider failure (missing key, HTTP error, bad payload)."""


def _call_groq(system_prompt: str, user_prompt: str) -> str:
    s = get_settings()
    if not s.groq_api_key:
        raise LLMError("GROQ_API_KEY is not set. Add it to your .env file.")
    payload = {
        "model": s.groq_model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": s.temperature,
        "max_tokens": s.max_tokens,
        "response_format": {"type": "json_object"},  # ask Groq for valid JSON
    }
    headers = {"Authorization": f"Bearer {s.groq_api_key}"}
    try:
        r = httpx.post(GROQ_URL, json=payload, headers=headers, timeout=s.timeout)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except httpx.HTTPStatusError as e:
        raise LLMError(f"Groq HTTP {e.response.status_code}: {e.response.text[:300]}") from e
    except (httpx.HTTPError, KeyError, IndexError, ValueError) as e:
        raise LLMError(f"Groq request failed: {e}") from e


def _call_gemini(system_prompt: str, user_prompt: str) -> str:
    s = get_settings()
    if not s.gemini_api_key:
        raise LLMError("GEMINI_API_KEY is not set. Add it to your .env file.")
    payload = {
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
        "generationConfig": {
            "temperature": s.temperature,
            "maxOutputTokens": s.max_tokens,
            "responseMimeType": "application/json",  # ask Gemini for valid JSON
        },
    }
    headers = {"x-goog-api-key": s.gemini_api_key}
    url = GEMINI_URL.format(model=s.gemini_model)
    try:
        r = httpx.post(url, json=payload, headers=headers, timeout=s.timeout)
        r.raise_for_status()
        return r.json()["candidates"][0]["content"]["parts"][0]["text"]
    except httpx.HTTPStatusError as e:
        raise LLMError(f"Gemini HTTP {e.response.status_code}: {e.response.text[:300]}") from e
    except (httpx.HTTPError, KeyError, IndexError, ValueError) as e:
        raise LLMError(f"Gemini request failed: {e}") from e


def _call_mock(system_prompt: str, user_prompt: str) -> str:
    """Offline stand-in so the API can be demoed/tested without any key."""
    return (
        '{"answer": "This is a mock reply (LLM_PROVIDER=mock). '
        'Set LLM_PROVIDER=groq or gemini for real answers.", '
        '"confidence": 0.5, "follow_up": "Would you like to try a real provider?"}'
    )


_PROVIDERS = {"groq": _call_groq, "gemini": _call_gemini, "mock": _call_mock}


def generate(system_prompt: str, user_prompt: str) -> str:
    """Send the prompts to the configured provider and return the raw text."""
    provider = get_settings().provider
    fn = _PROVIDERS.get(provider)
    if fn is None:
        raise LLMError(f"Unknown LLM_PROVIDER '{provider}'. Use one of: {', '.join(_PROVIDERS)}.")
    return fn(system_prompt, user_prompt)
