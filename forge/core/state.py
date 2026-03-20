from __future__ import annotations

from datetime import datetime, timezone
from typing import Annotated
from typing import Literal

from pydantic import BaseModel, Field


class TokenBudget(BaseModel):
    total_allocated: int
    total_used: int = 0
    per_agent: dict[str, int] = Field(default_factory=dict)
    is_exceeded: bool = False


class AgentError(BaseModel):
    agent_name: str
    error_type: str
    message: str
    timestamp: datetime
    retry_count: int = 0


class Feature(BaseModel):
    name: str
    description: str
    priority: Literal["must_have", "should_have", "nice_to_have"]
    acceptance_criteria: list[str]


class PRDSchema(BaseModel):
    version: str = "1.0"
    project_name: str
    one_liner: str
    target_users: str
    core_features: list[Feature]
    out_of_scope: list[str]
    success_metrics: list[str]
    tech_constraints: list[str]
    acceptance_criteria: list[str]
    estimated_complexity: Literal["simple", "medium", "complex"]
    estimated_credits: int
    skill_hints: list[str]


class DataModel(BaseModel):
    name: str
    fields: dict[str, str]
    relationships: list[str]
    supabase_rls_policy: str | None = None


class APIRoute(BaseModel):
    method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
    path: str
    description: str
    auth_required: bool
    request_body: dict | None = None
    response_schema: dict


class TechSpecSchema(BaseModel):
    version: str = "1.0"
    stack: dict = Field(
        default_factory=lambda: {
            "frontend": "Next.js 15",
            "backend": "Supabase",
            "deploy": "Vercel",
        }
    )
    data_models: list[DataModel]
    api_routes: list[APIRoute]
    component_tree: dict
    env_vars_needed: list[str]
    third_party_integrations: list[str]
    estimated_files: int
    supabase_schema_sql: str
    agent_task_breakdown: dict[str, list[str]]
    skill_assignments: dict[str, str]


class DesignToken(BaseModel):
    colors: dict[str, str]
    spacing: dict[str, str]
    typography: dict[str, dict]
    radii: dict[str, str]
    shadows: dict[str, str]


class WireframeSchema(BaseModel):
    version: str = "1.0"
    mode: Literal["figma", "screenshot", "prd_only"]
    design_tokens: DesignToken
    component_list: list[str]
    layout_description: str
    visual_similarity_score: float | None = None
    figma_file_key: str | None = None
    spec_document: str


class SecurityFinding(BaseModel):
    severity: Literal["critical", "high", "medium", "low", "info"]
    rule_id: str
    file_path: str
    line_number: int
    description: str
    remediation: str
    owasp_category: str | None = None


class SecurityReport(BaseModel):
    version: str = "1.0"
    verdict: Literal["PASS", "FAIL"]
    critical_count: int
    high_count: int
    findings: list[SecurityFinding]
    owasp_checks_passed: list[str]
    owasp_checks_failed: list[str]
    snyk_report_url: str | None = None
    semgrep_rules_run: int


class TestCase(BaseModel):
    name: str
    type: Literal["unit", "integration", "e2e"]
    status: Literal["passed", "failed", "skipped"]
    duration_ms: int
    error_message: str | None = None


class TestResults(BaseModel):
    version: str = "1.0"
    verdict: Literal["PASS", "FAIL"]
    total_tests: int
    passed: int
    failed: int
    skipped: int
    coverage_percent: Annotated[float, Field(ge=0.0, le=100.0)]
    test_cases: list[TestCase]
    e2b_session_id: str
    iterations_needed: int


class CriticVerdict(BaseModel):
    version: str = "1.0"
    verdict: Literal["APPROVE", "REJECT"]
    confidence: Annotated[float, Field(ge=0.0, le=1.0)]
    summary: str
    issues: list[str]
    risk_level: Literal["low", "medium", "high"]
    rollback_plan: str
    estimated_deploy_time_mins: int


class HITLPayload(BaseModel):
    project_id: str
    project_name: str
    critic_summary: str
    risk_level: str
    files_changed: list[str]
    lines_added: int
    lines_removed: int
    git_diff_url: str
    git_commit_sha: str
    security_status: str
    test_coverage: float
    rollback_plan: str
    estimated_deploy_time: str
    skills_used: list[str]


class SkillMetadata(BaseModel):
    id: str
    name: str
    description: str
    category: str
    tags: list[str]
    stack_requirements: list[str]
    success_rate: Annotated[float, Field(ge=0.0, le=100.0)] = 0.0
    last_updated: datetime


class ForgeState(BaseModel):
    project_id: str
    user_id: str
    session_id: str
    created_at: datetime

    user_input: str
    input_type: Literal["text", "screenshot", "voice", "email", "figma_url"] = "text"

    prd: PRDSchema | None = None
    tech_spec: TechSpecSchema | None = None
    wireframes: WireframeSchema | None = None
    frontend_code: dict | None = None
    backend_code: dict | None = None
    security_report: SecurityReport | None = None
    test_results: TestResults | None = None
    critic_verdict: CriticVerdict | None = None

    skill_used: str | None = None
    skill_level: Annotated[int, Field(ge=1, le=3)] | None = None

    hitl_status: Literal["not_started", "pending", "approved", "rejected", "steered"] = "not_started"
    hitl_approval_token: str | None = None
    hitl_approver_id: str | None = None
    hitl_timestamp: datetime | None = None
    hitl_steer_notes: str | None = None

    deploy_url: str | None = None
    deploy_timestamp: datetime | None = None
    git_commit_sha: str | None = None

    token_budget: TokenBudget
    errors: list[AgentError] = Field(default_factory=list)
    current_agent: str | None = None
    pipeline_status: Literal["running", "paused", "completed", "failed"] = "running"
    iteration_count: int = 0


def make_initial_state(
    *,
    project_id: str,
    user_id: str,
    session_id: str,
    user_input: str,
    total_allocated_tokens: int,
    input_type: Literal["text", "screenshot", "voice", "email", "figma_url"] = "text",
) -> ForgeState:
    return ForgeState(
        project_id=project_id,
        user_id=user_id,
        session_id=session_id,
        created_at=datetime.now(tz=timezone.utc),
        user_input=user_input,
        input_type=input_type,
        token_budget=TokenBudget(total_allocated=total_allocated_tokens),
    )
