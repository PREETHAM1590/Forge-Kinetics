from __future__ import annotations

import uuid

from forge.agents.finops import FinOpsAgent
from forge.core.state import make_initial_state


def test_finops_record_usage_per_agent() -> None:
	state = make_initial_state(
		project_id=str(uuid.uuid4()),
		user_id="finops-user",
		session_id=str(uuid.uuid4()),
		user_input="Track usage",
		total_allocated_tokens=500,
	)
	agent = FinOpsAgent()
	agent.record_usage(state, "pm_agent", 120)
	agent.record_usage(state, "pm_agent", 80)

	assert state.token_budget.per_agent["pm_agent"] == 200
	assert state.token_budget.total_used == 200
	assert state.token_budget.is_exceeded is False


def test_finops_budget_exceeded_flag() -> None:
	state = make_initial_state(
		project_id=str(uuid.uuid4()),
		user_id="finops-user",
		session_id=str(uuid.uuid4()),
		user_input="Track usage",
		total_allocated_tokens=100,
	)
	agent = FinOpsAgent()
	agent.record_usage(state, "architect_agent", 101)
	assert state.token_budget.is_exceeded is True
