from __future__ import annotations

import os
from pathlib import Path


GEMINI_MODEL = "gemini-1.5-flash"
OPENROUTER_MODEL = "mistralai/mistral-7b-instruct"
ENV_FILE = Path(__file__).resolve().parents[1] / ".env"


def _load_dotenv() -> None:
    if not ENV_FILE.exists():
        return

    for raw_line in ENV_FILE.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()

        if not key:
            continue

        if value and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]

        os.environ.setdefault(key, value)


def _require_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise EnvironmentError(f"Missing required environment variable: {name}")
    return value


_load_dotenv()
GEMINI_API_KEY = _require_env("GEMINI_API_KEY")
OPENROUTER_API_KEY = _require_env("OPENROUTER_API_KEY")
