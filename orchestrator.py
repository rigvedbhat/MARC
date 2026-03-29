from __future__ import annotations

from agents.agent_manager import run_all_agents
from core.critique_engine import generate_critique
from core.merge_engine import merge_responses
from core.refinement_engine import refine_all
from core.response_pool import ResponsePool


def _print_responses(title: str, responses: list[dict]) -> None:
    print(f"\n=== {title} ===")
    for index, item in enumerate(responses, start=1):
        print(f"\n[{index}] {item['label']}")
        print(item["response"])


def _parse_selection(selection: str, total: int) -> list[int] | None:
    raw_parts = selection.replace(",", " ").split()
    if len(raw_parts) != 2:
        return None

    try:
        numbers = [int(part) for part in raw_parts]
    except ValueError:
        return None

    if numbers[0] == numbers[1]:
        return None

    indices = [number - 1 for number in numbers]
    if any(index < 0 or index >= total for index in indices):
        return None

    return indices


def _select_two_responses(responses: list[dict]) -> list[dict]:
    prompt_text = "Select exactly 2 responses by number (example: 1 2): "

    for attempt in range(2):
        selection = input(prompt_text).strip()
        indices = _parse_selection(selection, len(responses))
        if indices is not None:
            return [responses[index] for index in indices]

        if attempt == 0:
            print("Invalid selection. Please enter exactly two different valid response numbers.")

    raise ValueError("Unable to continue: invalid response selection entered twice.")


async def run(prompt: str, pool: ResponsePool) -> None:
    v1_responses = await run_all_agents(prompt)
    pool.store_v1(v1_responses)

    _print_responses("V1 Responses", v1_responses)
    selected_responses = _select_two_responses(v1_responses)

    critique = await generate_critique(prompt, selected_responses)
    print("\n=== Critique ===")
    print(critique)

    v2_responses = await refine_all(prompt, v1_responses, critique)
    pool.store_v2(v2_responses)

    v3_response = await merge_responses(prompt, v2_responses)
    pool.store_v3(v3_response)

    print("\n=== V3 Merged Response ===")
    print(v3_response)

    show_versions = input("\nWould you like to see all versions? (y/n): ").strip().lower()
    if show_versions in {"y", "yes"}:
        pool.print_all_versions()
