from __future__ import annotations

import asyncio

from agents.gemini_agent import call_gemini
from agents.openrouter_agent import call_openrouter
from utils.config import OPENROUTER_MODEL


GEMINI_LABEL = "Gemini"


def _build_openrouter_label() -> str:
    model_name = OPENROUTER_MODEL.split("/", 1)[-1]
    if model_name.endswith("-instruct"):
        model_name = model_name[: -len("-instruct")]
    return f"OpenRouter ({model_name})"


OPENROUTER_LABEL = _build_openrouter_label()


async def run_all_agents(prompt: str) -> list[dict]:
    results = await asyncio.gather(
        call_gemini(prompt),
        call_openrouter(prompt),
        return_exceptions=True,
    )

    labels = [GEMINI_LABEL, OPENROUTER_LABEL]
    responses: list[dict] = []

    for label, result in zip(labels, results):
        if isinstance(result, Exception):
            responses.append({"label": label, "response": f"[ERROR: {result}]"})
        else:
            responses.append({"label": label, "response": result})

    return responses
