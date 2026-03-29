from __future__ import annotations

from agents.gemini_agent import call_gemini
from utils.prompts import build_merge_prompt


async def merge_responses(original_prompt: str, refined_responses: list[dict]) -> str:
    """
    Builds merge prompt using prompts.build_merge_prompt.
    Calls Gemini to generate the merged response.
    Returns the merged string.
    """
    merge_prompt = build_merge_prompt(original_prompt, refined_responses)
    return await call_gemini(merge_prompt)
