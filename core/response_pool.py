from __future__ import annotations


class ResponsePool:
    def __init__(self) -> None:
        self._v1: list[dict] = []
        self._v2: list[dict] = []
        self._v3: str = ""

    @staticmethod
    def _copy_responses(responses: list[dict]) -> list[dict]:
        return [{"label": item["label"], "response": item["response"]} for item in responses]

    @staticmethod
    def _print_responses(responses: list[dict]) -> None:
        if not responses:
            print("[Not generated]")
            return

        for index, item in enumerate(responses, start=1):
            print(f"\n[{index}] {item['label']}")
            print(item["response"])

    def store_v1(self, responses: list[dict]) -> None:
        self._v1 = self._copy_responses(responses)

    def store_v2(self, responses: list[dict]) -> None:
        self._v2 = self._copy_responses(responses)

    def store_v3(self, merged: str) -> None:
        self._v3 = merged

    def get_v1(self) -> list[dict]:
        return self._copy_responses(self._v1)

    def get_v2(self) -> list[dict]:
        return self._copy_responses(self._v2)

    def get_v3(self) -> str:
        return self._v3

    def print_all_versions(self) -> None:
        """Prints v1, v2, and v3 clearly labeled to stdout."""
        print("\n=== V1 Responses ===")
        self._print_responses(self._v1)

        print("\n\n=== V2 Refined Responses ===")
        self._print_responses(self._v2)

        print("\n\n=== V3 Merged Response ===")
        if self._v3:
            print(self._v3)
        else:
            print("[Not generated]")
