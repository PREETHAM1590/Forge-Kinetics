from __future__ import annotations

from dataclasses import dataclass

from forge.core.state import ForgeState


@dataclass(slots=True)
class FinOpsAgent:
    """Tracks token usage and flips budget exceeded flag when needed."""

    def record_usage(self, state: ForgeState, agent_name: str, tokens_used: int) -> ForgeState:
        per_agent_used = state.token_budget.per_agent.get(agent_name, 0) + tokens_used
        state.token_budget.per_agent[agent_name] = per_agent_used
        state.token_budget.total_used += tokens_used
        state.token_budget.is_exceeded = state.token_budget.total_used > state.token_budget.total_allocated
        state.current_agent = "finops_agent"
        return state
