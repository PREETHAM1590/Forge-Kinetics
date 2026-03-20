from __future__ import annotations

import uuid

from forge.agents.finops import FinOpsAgent
from forge.core.state import make_initial_state


def test_make_initial_state_defaults() -> None:
	state = make_initial_state(
		project_id=str(uuid.uuid4()),
		user_id="state-user",
		session_id=str(uuid.uuid4()),
		user_input="Build a test app",
		total_allocated_tokens=1000,
	)
	assert state.pipeline_status == "running"
	assert state.hitl_status == "not_started"
	assert state.token_budget.total_used == 0


def test_token_budget_updates_with_finops() -> None:
	state = make_initial_state(
		project_id=str(uuid.uuid4()),
		user_id="state-user",
		session_id=str(uuid.uuid4()),
		user_input="Build a test app",
		total_allocated_tokens=100,
	)
	finops = FinOpsAgent()
	finops.record_usage(state, "pm_agent", 60)
	finops.record_usage(state, "architect_agent", 50)

	assert state.token_budget.total_used == 110
	assert state.token_budget.is_exceeded is True
	assert state.token_budget.per_agent["pm_agent"] == 60
