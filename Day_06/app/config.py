"""Central settings, read from environment variables (and a local .env file)."""
import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parent.parent
load_dotenv(ROOT_DIR / ".env")  # silently does nothing if .env is absent


@dataclass(frozen=True)
class Settings:
    provider: str
    groq_api_key: str
    groq_model: str
    gemini_api_key: str
    gemini_model: str
    temperature: float
    max_tokens: int
    timeout: float
    prompts_dir: Path


def get_settings() -> Settings:
    """Read settings fresh each call so tests / env changes take effect."""
    return Settings(
        provider=os.getenv("LLM_PROVIDER", "groq").strip().lower(),
        groq_api_key=os.getenv("GROQ_API_KEY", "").strip(),
        groq_model=os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip(),
        gemini_api_key=os.getenv("GEMINI_API_KEY", "").strip(),
        gemini_model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip(),
        temperature=float(os.getenv("LLM_TEMPERATURE", "0.2")),
        max_tokens=int(os.getenv("LLM_MAX_TOKENS", "700")),
        timeout=float(os.getenv("LLM_TIMEOUT_SECONDS", "30")),
        prompts_dir=ROOT_DIR / "prompts",
    )
