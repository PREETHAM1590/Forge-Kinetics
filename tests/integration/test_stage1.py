from __future__ import annotations

import uuid

from forge.agents.architect import ArchitectAgent
from forge.agents.pm_agent import PMAgent
from forge.core.state import make_initial_state


def test_stage1_pm_and_architect_flow() -> None:
	state = make_initial_state(
		project_id=str(uuid.uuid4()),
		user_id="stage1-user",
		session_id=str(uuid.uuid4()),
		user_input="Build a todo app with auth and dashboard",
		total_allocated_tokens=2000,
	)

	state = PMAgent().run(state)
	assert state.prd is not None
	assert state.prd.project_name
	assert len(state.prd.core_features) >= 1

	state = ArchitectAgent().run(state)
	assert state.tech_spec is not None
	assert state.tech_spec.stack["frontend"] == "Next.js 15"
	assert state.tech_spec.stack["backend"] == "Supabase"
	assert len(state.tech_spec.api_routes) >= 2
	assert "create table if not exists" in state.tech_spec.supabase_schema_sql
