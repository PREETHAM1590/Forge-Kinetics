from __future__ import annotations

import uuid

from forge.agents.devops import DevOpsAgent
from forge.core.graph import run_pipeline
from forge.core.state import make_initial_state
from forge.hitl.gate import HITLGate


def test_full_pipeline_requires_hitl_then_deploys() -> None:
	state = make_initial_state(
		project_id=str(uuid.uuid4()),
		user_id="full-user",
		session_id=str(uuid.uuid4()),
		user_input="Build project dashboard with auth",
		total_allocated_tokens=8000,
	)

	result = run_pipeline(state)
	assert result.prd is not None
	assert result.tech_spec is not None
	assert result.hitl_status == "pending"
	assert result.pipeline_status == "paused"

	gate = HITLGate()
	result.hitl_status = "approved"
	result.hitl_approval_token = gate.generate_approval_token(result.project_id, "approver-1")
	deployed = DevOpsAgent().run(result)
	assert deployed.pipeline_status == "completed"
	assert deployed.deploy_url is not None
