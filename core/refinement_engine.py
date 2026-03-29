from __future__ import annotations

import asyncio

from agents.gemini_agent import call_gemini
from agents.openrouter_agent import call_openrouter
from utils.prompts import build_refinement_prompt


def _resolve_agent(label: str):
    if label == "Gemini":
        return call_gemini
    if label.startswith("OpenRouter"):
        return call_openrouter
    raise ValueError(f"Unknown agent label: {label}")


async def _refine_one(original_prompt: str, item: dict, critique: str) -> dict:
    label = item["label"]
    response = item["response"]
    agent = _resolve_agent(label)
    refinement_prompt = build_refinement_prompt(original_prompt, response, critique)

    try:
        refined_response = await agent(refinement_prompt)
    except Exception as exc:
        refined_response = f"[ERROR: {exc}]"

    return {"label": label, "response": refined_response}


async def refine_all(original_prompt: str, v1_responses: list[dict], critique: str) -> list[dict]:
    """
    For each response in v1_responses:
    - Build a refinement prompt using prompts.build_refinement_prompt
    - Call the appropriate agent (match by label string, not index)
    - Return list of dicts: [{"label": str, "response": str}]
    Run all refinements in parallel using asyncio.gather.
    """
    tasks = [
        _refine_one(original_prompt=original_prompt, item=item, critique=critique)
        for item in v1_responses
    ]
    return await asyncio.gather(*tasks)
