from __future__ import annotations

from pydantic import BaseModel

from forge.core.state import ForgeState


class HITLReviewPayload(BaseModel):
	project_id: str
	project_name: str
	critic_summary: str
	risk_level: str
	security_status: str
	test_coverage: float


def build_hitl_payload(state: ForgeState) -> HITLReviewPayload:
	return HITLReviewPayload(
		project_id=state.project_id,
		project_name=state.prd.project_name if state.prd else "Unknown",
		critic_summary=state.critic_verdict.summary if state.critic_verdict else "",
		risk_level=state.critic_verdict.risk_level if state.critic_verdict else "unknown",
		security_status=state.security_report.verdict if state.security_report else "UNKNOWN",
		test_coverage=state.test_results.coverage_percent if state.test_results else 0.0,
	)

