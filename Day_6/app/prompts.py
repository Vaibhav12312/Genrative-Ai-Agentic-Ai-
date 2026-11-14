"""Loads prompt files from the prompts/ folder."""
from functools import lru_cache

from app.config import get_settings

# API version label -> task prompt file
TASK_PROMPTS = {"v1": "task_v1.md", "v2": "task_v2.md"}


@lru_cache(maxsize=None)
def _read(filename: str) -> str:
    return (get_settings().prompts_dir / filename).read_text(encoding="utf-8").strip()


def load_system_prompt() -> str:
    return _read("system.md")


def build_user_prompt(question: str, version: str = "v2") -> str:
    if version not in TASK_PROMPTS:
        raise ValueError(f"Unknown prompt version '{version}'. Use: {', '.join(TASK_PROMPTS)}")
    # str.replace (not .format) so JSON braces inside the template are safe
    return _read(TASK_PROMPTS[version]).replace("{question}", question.strip())
