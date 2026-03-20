from __future__ import annotations

from dataclasses import dataclass, field

from forge.memory.log import MemoryLog


@dataclass(slots=True)
class MemoryCore:
	"""Tier-1 core memory context shared during a pipeline execution."""

	context: dict[str, str] = field(default_factory=dict)
	log: MemoryLog = field(default_factory=MemoryLog)

	async def put(self, key: str, value: str) -> None:
		self.context[key] = value
		await self.log.append("core.put", {"key": key})

	async def get(self, key: str) -> str | None:
		return self.context.get(key)

