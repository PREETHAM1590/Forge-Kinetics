from __future__ import annotations

import uuid

from forge.agents.devops import DevOpsAgent
from forge.core.graph import run_pipeline
from forge.core.state import make_initial_state
from forge.hitl.gate import HITLGate


def test_stage5_pipeline_pauses_without_approval() -> None:
    state = make_initial_state(
        project_id=str(uuid.uuid4()),
        user_id="stage5-user",
        session_id=str(uuid.uuid4()),
        user_input="Build a dashboard with auth and billing",
        total_allocated_tokens=6000,
    )

    result = run_pipeline(state)

    assert result.hitl_status == "pending"
    assert result.pipeline_status == "paused"
    assert result.deploy_url is None


def test_stage5_devops_deploys_with_approval_token() -> None:
    gate = HITLGate()
    project_id = str(uuid.uuid4())

    state = make_initial_state(
        project_id=project_id,
        user_id="stage5-user",
        session_id=str(uuid.uuid4()),
        user_input="Deploy test",
        total_allocated_tokens=1000,
    )
    state.hitl_status = "approved"
    state.hitl_approval_token = gate.generate_approval_token(project_id=project_id, approver_id="human-1")

    result = DevOpsAgent().run(state)

    assert result.pipeline_status == "completed"
    assert result.deploy_url is not None
