from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class CollectiveBrain:
    patterns: list[dict[str, Any]] = field(default_factory=list)
    skill_updates: dict[str, list[dict[str, Any]]] = field(default_factory=dict)

    def contribute_build_patterns(self, project_id: str, patterns: dict[str, Any]) -> None:
        self.patterns.append({"project_id": project_id, "patterns": patterns})

    def update_skill(self, skill_id: str, fix: dict[str, Any]) -> None:
        self.skill_updates.setdefault(skill_id, []).append(fix)
