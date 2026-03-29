from __future__ import annotations

import google.generativeai as genai

from utils.config import GEMINI_API_KEY, GEMINI_MODEL


genai.configure(api_key=GEMINI_API_KEY)
_MODEL = genai.GenerativeModel(GEMINI_MODEL)


def _extract_text(result: object) -> str:
    text = getattr(result, "text", None)
    if isinstance(text, str) and text.strip():
        return text.strip()

    candidates = getattr(result, "candidates", None) or []
    chunks: list[str] = []

    for candidate in candidates:
        content = getattr(candidate, "content", None)
        parts = getattr(content, "parts", None) or []
        for part in parts:
            part_text = getattr(part, "text", None)
            if isinstance(part_text, str) and part_text.strip():
                chunks.append(part_text.strip())

    if chunks:
        return "\n".join(chunks).strip()

    raise ValueError("Gemini returned an empty response.")


async def call_gemini(prompt: str) -> str:
    """Calls Gemini 1.5 Flash. Returns the response text. Raises on failure."""
    try:
        result = await _MODEL.generate_content_async(prompt)
        return _extract_text(result)
    except Exception as exc:
        raise RuntimeError(f"Gemini call failed: {exc}") from exc
