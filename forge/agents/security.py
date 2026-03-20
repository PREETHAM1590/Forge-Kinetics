from __future__ import annotations

from dataclasses import dataclass

from forge.core.state import ForgeState, SecurityReport


@dataclass(slots=True)
class SecurityAgent:
    """Stage 4 security scaffold that builds a deterministic SecurityReport."""

    def run(self, state: ForgeState) -> ForgeState:
        findings = []
        critical_count = 0
        high_count = 0

        frontend_status = (state.frontend_code or {}).get("status")
        backend_status = (state.backend_code or {}).get("status")
        if frontend_status == "needs_attention" or backend_status == "needs_attention":
            high_count += 1

        verdict = "FAIL" if (critical_count > 0 or high_count > 0) else "PASS"

        state.security_report = SecurityReport(
            verdict=verdict,
            critical_count=critical_count,
            high_count=high_count,
            findings=findings,
            owasp_checks_passed=["A01", "A05", "A07"] if verdict == "PASS" else ["A01", "A05"],
            owasp_checks_failed=[] if verdict == "PASS" else ["A07"],
            semgrep_rules_run=25,
            snyk_report_url=None,
        )
        state.current_agent = "security_agent"
        return state
