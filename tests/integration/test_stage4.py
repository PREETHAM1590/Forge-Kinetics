from __future__ import annotations

import uuid

from forge.agents.critic import CriticAgent
from forge.core.graph import run_pipeline
from forge.core.state import (
    SecurityReport,
    TestCase as StageTestCase,
    TestResults as StageTestResults,
    make_initial_state,
)


def test_stage4_pipeline_quality_smoke() -> None:
    state = make_initial_state(
        project_id=str(uuid.uuid4()),
        user_id="stage4-user",
        session_id=str(uuid.uuid4()),
        user_input="Build a dashboard with auth",
        total_allocated_tokens=5000,
    )

    result = run_pipeline(state)

    assert result.security_report is not None
    assert result.test_results is not None
    assert result.critic_verdict is not None
    assert result.critic_verdict.verdict in {"APPROVE", "REJECT"}


def test_critic_rejects_security_failure() -> None:
    state = make_initial_state(
        project_id=str(uuid.uuid4()),
        user_id="critic-user",
        session_id=str(uuid.uuid4()),
        user_input="test",
        total_allocated_tokens=1000,
    )

    state.security_report = SecurityReport(
        verdict="FAIL",
        critical_count=1,
        high_count=0,
        findings=[],
        owasp_checks_passed=[],
        owasp_checks_failed=["A01"],
        semgrep_rules_run=10,
    )
    state.test_results = StageTestResults(
        verdict="PASS",
        total_tests=4,
        passed=4,
        failed=0,
        skipped=0,
        coverage_percent=85.0,
        test_cases=[StageTestCase(name="x", type="unit", status="passed", duration_ms=10)],
        e2b_session_id="abc",
        iterations_needed=1,
    )

    result = CriticAgent().run(state)
    assert result.critic_verdict is not None
    assert result.critic_verdict.verdict == "REJECT"
