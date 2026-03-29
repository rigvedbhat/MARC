from __future__ import annotations

import httpx

from utils.config import OPENROUTER_API_KEY, OPENROUTER_MODEL


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"


def _extract_content(payload: dict) -> str:
    choices = payload.get("choices", [])
    if not choices:
        raise ValueError("OpenRouter returned no choices.")

    message = choices[0].get("message", {})
    content = message.get("content", "")

    if isinstance(content, str) and content.strip():
        return content.strip()

    if isinstance(content, list):
        text_parts: list[str] = []
        for item in content:
            if isinstance(item, dict) and isinstance(item.get("text"), str):
                text_value = item["text"].strip()
                if text_value:
                    text_parts.append(text_value)
        if text_parts:
            return "\n".join(text_parts).strip()

    raise ValueError("OpenRouter returned an empty response.")


async def call_openrouter(prompt: str) -> str:
    """Calls OpenRouter. Returns response text. Raises on failure."""
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(OPENROUTER_URL, headers=headers, json=payload)
    except Exception as exc:
        raise RuntimeError(f"OpenRouter call failed: {exc}") from exc

    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter call failed: {response.status_code} {response.text}")

    try:
        return _extract_content(response.json())
    except Exception as exc:
        raise RuntimeError(f"OpenRouter call failed: {exc}") from exc
