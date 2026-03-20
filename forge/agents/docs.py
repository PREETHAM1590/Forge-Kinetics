from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DocsAgent:
    async def generate_on_commit(self, diff: str) -> str:
        lines = [
            "# Auto Docs Update",
            "",
            "## Summary",
            f"Processed diff length: {len(diff)}",
        ]
        return "\n".join(lines)
