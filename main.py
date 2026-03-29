from __future__ import annotations

import asyncio


def main() -> None:
    try:
        import orchestrator
        from core.response_pool import ResponsePool

        prompt = input("Enter your prompt: ").strip()
        if not prompt:
            raise ValueError("Prompt cannot be empty.")

        pool = ResponsePool()
        asyncio.run(orchestrator.run(prompt, pool))
    except Exception as exc:
        print(f"Error: {exc}")


if __name__ == "__main__":
    main()
