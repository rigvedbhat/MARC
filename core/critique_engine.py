from __future__ import annotations

from agents.gemini_agent import call_gemini
from utils.prompts import build_critique_prompt


async def generate_critique(original_prompt: str, selected: list[dict]) -> str:
    """
    selected is a list of exactly 2 dicts: [{"label": str, "response": str}]
    Builds the critique prompt using prompts.build_critique_prompt.
    Calls Gemini to generate the critique.
    Returns the critique as a plain string.
    """
    if len(selected) != 2:
        raise ValueError("Critique generation requires exactly 2 selected responses.")

    critique_prompt = build_critique_prompt(
        prompt=original_prompt,
        response_a=selected[0]["response"],
        label_a=selected[0]["label"],
        response_b=selected[1]["response"],
        label_b=selected[1]["label"],
    )
    return await call_gemini(critique_prompt)
