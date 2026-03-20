from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from forge.agents.finops import FinOpsAgent
from forge.core.state import AgentError, ForgeState


@dataclass(slots=True)
class Observation:
    state_snapshot: dict[str, Any]
    notes: str = ""


@dataclass(slots=True)
class Action:
    kind: str
    payload: dict[str, Any]


@dataclass(slots=True)
class AgentResult:
    task_complete: bool
    tokens_used: int
    output: dict[str, Any]


class BudgetExceededError(RuntimeError):
    pass


class MaxIterationsError(RuntimeError):
    pass


class BaseAgent:
    """OpenHands-style asynchronous base loop for build agents."""

    name: str = "base_agent"
    max_iterations: int = 20

    def __init__(self, finops: FinOpsAgent | None = None) -> None:
        self.finops = finops or FinOpsAgent()

    async def run(self, state: ForgeState) -> ForgeState:
        for iteration in range(self.max_iterations):
            state.iteration_count = iteration + 1
            state.current_agent = self.name

            try:
                observation = await self.observe(state)
                action = await self.think(observation, state)
                result = await self.act(action, state)
                self.finops.record_usage(
                    state=state,
                    agent_name=self.name,
                    tokens_used=max(result.tokens_used, 0),
                )
            except ValueError as error:
                state.errors.append(
                    AgentError(
                        agent_name=self.name,
                        error_type="ValueError",
                        message=str(error),
                        timestamp=state.created_at,
                    )
                )
                raise

            if result.task_complete:
                return await self.validate_output(result, state)

            if state.token_budget.is_exceeded:
                raise BudgetExceededError(f"{self.name} exceeded token budget")

        raise MaxIterationsError(f"{self.name} hit max iterations: {self.max_iterations}")

    async def observe(self, state: ForgeState) -> Observation:
        return Observation(state_snapshot=state.model_dump())

    async def think(self, observation: Observation, state: ForgeState) -> Action:
        raise NotImplementedError

    async def act(self, action: Action, state: ForgeState) -> AgentResult:
        raise NotImplementedError

    async def validate_output(self, result: AgentResult, state: ForgeState) -> ForgeState:
        return state
