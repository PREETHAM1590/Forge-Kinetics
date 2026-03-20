from __future__ import annotations

from dataclasses import dataclass

from forge.core.state import ForgeState, TestCase, TestResults


@dataclass(slots=True)
class TestingAgent:
    """Stage 4 testing scaffold that emits deterministic TestResults."""

    def run(self, state: ForgeState) -> ForgeState:
        frontend_ok = (state.frontend_code or {}).get("status") == "built"
        backend_ok = (state.backend_code or {}).get("status") == "built"

        passed = 4 if (frontend_ok and backend_ok) else 2
        failed = 0 if (frontend_ok and backend_ok) else 2
        total = passed + failed
        verdict = "PASS" if failed == 0 else "FAIL"
        coverage = 82.5 if verdict == "PASS" else 56.0

        test_cases = [
            TestCase(name="auth-flow", type="e2e", status="passed" if frontend_ok else "failed", duration_ms=480),
            TestCase(name="tasks-api", type="integration", status="passed" if backend_ok else "failed", duration_ms=210),
            TestCase(name="dashboard-render", type="unit", status="passed", duration_ms=95),
            TestCase(name="billing-route", type="integration", status="passed" if backend_ok else "failed", duration_ms=160),
        ]

        state.test_results = TestResults(
            verdict=verdict,
            total_tests=total,
            passed=passed,
            failed=failed,
            skipped=0,
            coverage_percent=coverage,
            test_cases=test_cases,
            e2b_session_id=f"test-session-{state.session_id[:8]}",
            iterations_needed=1,
        )
        state.current_agent = "testing_agent"
        return state
