from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

from forge.core.state import ForgeState
from forge.hitl.gate import HITLGate


@dataclass(slots=True)
class DevOpsAgent:
    """Stage 5 deploy scaffold gated strictly by HITL approval."""

    def run(self, state: ForgeState) -> ForgeState:
        gate = HITLGate()
        approval = gate.require_approval(state)
        if not approval.approved:
            state.pipeline_status = "paused"
            state.current_agent = "devops_agent"
            return state

        state.deploy_url = f"https://{state.project_id[:8]}.forge.local"
        state.deploy_timestamp = datetime.now(tz=timezone.utc)
        state.pipeline_status = "completed"
        state.current_agent = "devops_agent"
        return state
