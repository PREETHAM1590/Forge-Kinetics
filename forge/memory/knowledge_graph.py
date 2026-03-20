from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class TemporalKnowledgeGraph:
    """Local in-memory scaffold for Tier-5 knowledge graph behavior."""

    decisions: dict[str, list[dict[str, Any]]] = field(default_factory=dict)
    brand_memory: dict[str, dict[str, Any]] = field(default_factory=dict)

    async def store_decision(self, project_id: str, decision: dict[str, Any]) -> None:
        self.decisions.setdefault(project_id, []).append(decision)

    async def get_client_context(self, project_id: str) -> dict[str, Any]:
        return {
            "project_id": project_id,
            "decisions": self.decisions.get(project_id, []),
            "brand_memory": self.brand_memory.get(project_id, {}),
        }

    async def store_brand_memory(self, project_id: str, brand: dict[str, Any]) -> None:
        current = self.brand_memory.get(project_id, {})
        current.update(brand)
        self.brand_memory[project_id] = current
