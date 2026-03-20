from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class WideResearchMode:
    async def research(self, main_query: str, depth: int = 5) -> str:
        queries = self._decompose_query(main_query, n=depth)
        return "\n".join([f"- {query}" for query in queries])

    def _decompose_query(self, query: str, n: int) -> list[str]:
        base = query.strip() or "general-research"
        return [f"{base} :: angle {i+1}" for i in range(max(1, n))]
