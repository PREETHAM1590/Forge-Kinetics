from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class TokenUsageTracker:
	total_allocated: int
	total_used: int = 0
	per_agent: dict[str, int] = field(default_factory=dict)

	def record(self, agent_name: str, tokens_used: int) -> dict[str, int | bool]:
		amount = max(tokens_used, 0)
		self.total_used += amount
		self.per_agent[agent_name] = self.per_agent.get(agent_name, 0) + amount
		return {
			"total_used": self.total_used,
			"remaining": max(self.total_allocated - self.total_used, 0),
			"is_exceeded": self.total_used > self.total_allocated,
		}

