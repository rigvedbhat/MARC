from __future__ import annotations


def build_critique_prompt(
    prompt: str,
    response_a: str,
    label_a: str,
    response_b: str,
    label_b: str,
) -> str:
    """
    Returns a structured critique prompt.
    The output must instruct the model to return exactly these sections:

    ## Strengths of {label_a}
    ## Weaknesses of {label_a}
    ## Strengths of {label_b}
    ## Weaknesses of {label_b}
    ## Missing Ideas (present in neither response)
    ## Suggested Improvements

    Do not ask for scores or rankings.
    """
    return f"""You are reviewing two independent answers to the same prompt.

Original prompt:
{prompt}

Response from {label_a}:
{response_a}

Response from {label_b}:
{response_b}

Compare the two responses constructively. Do not give scores, rankings, or declare a winner.
Return exactly these sections with the headings written verbatim:

## Strengths of {label_a}
## Weaknesses of {label_a}
## Strengths of {label_b}
## Weaknesses of {label_b}
## Missing Ideas (present in neither response)
## Suggested Improvements
"""


def build_refinement_prompt(original_prompt: str, original_response: str, critique: str) -> str:
    """
    Returns a prompt that instructs a model to improve its own response.
    Must include this instruction explicitly:
    'Do not copy the other model's response. Only integrate improvements that
    make your answer more accurate, complete, or clear.'
    """
    return f"""You are improving your own previous answer to a user prompt.

Original prompt:
{original_prompt}

Your previous response:
{original_response}

Critique to consider:
{critique}

Revise your answer into one stronger standalone response.
Do not copy the other model's response. Only integrate improvements that
make your answer more accurate, complete, or clear.
Return only the improved response.
"""


def build_merge_prompt(original_prompt: str, refined_responses: list[dict]) -> str:
    """
    refined_responses is a list of dicts: [{"label": str, "response": str}, ...]
    Returns a prompt that instructs a model to merge all refined responses into
    one single final answer. Must say: 'Remove redundancy. Preserve all unique
    insights. Do not attribute ideas to individual models.'
    """
    combined_responses = "\n\n".join(
        f"{item['label']}:\n{item['response']}" for item in refined_responses
    )

    return f"""You are merging multiple refined responses into one final answer for the user.

Original prompt:
{original_prompt}

Refined responses:
{combined_responses}

Create one single final answer.
Remove redundancy. Preserve all unique insights. Do not attribute ideas to individual models.
Return only the merged answer.
"""
