from __future__ import annotations

from dataclasses import dataclass

from forge.core.state import CriticVerdict, ForgeState


@dataclass(slots=True)
class CriticAgent:
    """Produces a quality-gate verdict using build, security, and test signals."""

    def run(self, state: ForgeState) -> ForgeState:
        issues: list[str] = []

        if state.prd is None or state.tech_spec is None:
            issues.append("Missing PRD or TechSpec")

        if state.security_report is None:
            issues.append("Missing security report")
        elif state.security_report.verdict != "PASS":
            issues.append("Security checks did not pass")

        if state.test_results is None:
            issues.append("Missing test results")
        else:
            if state.test_results.verdict != "PASS":
                issues.append("Tests did not pass")
            if state.test_results.coverage_percent < 70.0:
                issues.append("Coverage below minimum threshold (70%)")

        verdict = "APPROVE" if not issues else "REJECT"
        confidence = 0.9 if verdict == "APPROVE" else 0.35
        risk_level = "low" if verdict == "APPROVE" else "high"
        summary = "Quality gate passed: security + tests look good." if verdict == "APPROVE" else "Quality gate rejected due to validation issues."

        state.critic_verdict = CriticVerdict(
            verdict=verdict,
            confidence=confidence,
            summary=summary,
            issues=issues,
            risk_level=risk_level,
            rollback_plan="Revert to previous scaffold commit.",
            estimated_deploy_time_mins=15,
        )
        state.current_agent = "critic_agent"
        return state
