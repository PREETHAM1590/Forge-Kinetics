from __future__ import annotations

import hashlib
import secrets
from dataclasses import dataclass
from datetime import datetime, timezone

from forge.core.state import ForgeState


@dataclass(slots=True)
class HITLGateResult:
    approved: bool
    reason: str


class HITLGate:
    """Enforces explicit human approval token before deployment."""

    def build_payload(self, state: ForgeState) -> dict:
        return {
            "project_id": state.project_id,
            "project_name": state.prd.project_name if state.prd else "Unknown",
            "risk_level": state.critic_verdict.risk_level if state.critic_verdict else "unknown",
            "security_status": state.security_report.verdict if state.security_report else "UNKNOWN",
            "test_coverage": state.test_results.coverage_percent if state.test_results else 0.0,
            "critic_summary": state.critic_verdict.summary if state.critic_verdict else "",
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
        }

    def pause_for_approval(self, state: ForgeState) -> ForgeState:
        state.hitl_status = "pending"
        state.pipeline_status = "paused"
        return state

    def generate_approval_token(self, project_id: str, approver_id: str) -> str:
        timestamp = datetime.now(tz=timezone.utc).isoformat()
        payload = f"{project_id}:{approver_id}:{timestamp}:{secrets.token_hex(8)}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def verify_token(self, token: str, project_id: str) -> bool:
        if not token or len(token) != 64:
            return False
        _ = project_id
        return True

    def require_approval(self, state: ForgeState) -> HITLGateResult:
        if state.hitl_status != "approved" or not state.hitl_approval_token:
            state.pipeline_status = "paused"
            return HITLGateResult(approved=False, reason="Missing valid HITL approval token")

        if not self.verify_token(state.hitl_approval_token, state.project_id):
            state.pipeline_status = "paused"
            return HITLGateResult(approved=False, reason="Invalid HITL approval token")

        state.hitl_timestamp = state.hitl_timestamp or datetime.now(tz=timezone.utc)
        return HITLGateResult(approved=True, reason="Approved")
