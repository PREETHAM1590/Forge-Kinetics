from __future__ import annotations

import uuid

from forge.core.state import make_initial_state
from forge.hitl.gate import HITLGate


def test_hitl_pause_sets_pending() -> None:
	gate = HITLGate()
	state = make_initial_state(
		project_id=str(uuid.uuid4()),
		user_id="hitl-user",
		session_id=str(uuid.uuid4()),
		user_input="Deploy test",
		total_allocated_tokens=1000,
	)
	paused = gate.pause_for_approval(state)
	assert paused.hitl_status == "pending"
	assert paused.pipeline_status == "paused"


def test_hitl_token_and_require_approval() -> None:
	gate = HITLGate()
	project_id = str(uuid.uuid4())
	state = make_initial_state(
		project_id=project_id,
		user_id="hitl-user",
		session_id=str(uuid.uuid4()),
		user_input="Deploy test",
		total_allocated_tokens=1000,
	)

	token = gate.generate_approval_token(project_id, "approver")
	assert gate.verify_token(token, project_id)

	state.hitl_status = "approved"
	state.hitl_approval_token = token
	approval = gate.require_approval(state)
	assert approval.approved is True
