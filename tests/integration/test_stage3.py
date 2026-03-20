from __future__ import annotations

import uuid

from forge.core.graph import run_pipeline
from forge.core.state import make_initial_state


def test_stage3_pipeline_smoke() -> None:
    state = make_initial_state(
        project_id=str(uuid.uuid4()),
        user_id="test-user",
        session_id=str(uuid.uuid4()),
        user_input="Build a simple todo app with auth",
        total_allocated_tokens=5000,
    )

    result = run_pipeline(state)

    assert result.prd is not None
    assert result.tech_spec is not None
    assert result.frontend_code is not None
    assert result.backend_code is not None
    assert result.pipeline_status in {"completed", "failed", "paused"}
