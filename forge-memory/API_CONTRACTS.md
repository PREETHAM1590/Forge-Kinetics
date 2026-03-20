# API_CONTRACTS.md — Agent Pydantic Schemas v2.0
> All agent-to-agent schemas. Update when schemas change. Version them.

---

## MASTER STATE

```python
# forge/core/state.py

from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

class TokenBudget(BaseModel):
    total_allocated: int
    total_used: int
    per_agent: dict[str, int]  # agent_name → tokens used
    is_exceeded: bool = False

class AgentError(BaseModel):
    agent_name: str
    error_type: str
    message: str
    timestamp: datetime
    retry_count: int = 0

class ForgeState(BaseModel):
    # Identity
    project_id: str
    user_id: str
    session_id: str
    created_at: datetime

    # Input
    user_input: str
    input_type: Literal["text","screenshot","voice","email","figma_url"] = "text"

    # Agent outputs (None until agent runs)
    prd: "PRDSchema | None" = None
    tech_spec: "TechSpecSchema | None" = None
    wireframes: "WireframeSchema | None" = None
    frontend_code: dict | None = None
    backend_code: dict | None = None
    security_report: "SecurityReport | None" = None
    test_results: "TestResults | None" = None
    critic_verdict: "CriticVerdict | None" = None

    # Skills
    skill_used: str | None = None       # which skill.md was loaded
    skill_level: int | None = None      # 1, 2, or 3

    # HITL Gate
    hitl_status: Literal["not_started","pending","approved","rejected","steered"] = "not_started"
    hitl_approval_token: str | None = None
    hitl_approver_id: str | None = None
    hitl_timestamp: datetime | None = None
    hitl_steer_notes: str | None = None  # if STEER mode used

    # Deployment
    deploy_url: str | None = None
    deploy_timestamp: datetime | None = None
    git_commit_sha: str | None = None   # artifact commit

    # Operations
    token_budget: TokenBudget
    errors: list[AgentError] = Field(default_factory=list)
    current_agent: str | None = None
    pipeline_status: Literal["running","paused","completed","failed"] = "running"
    iteration_count: int = 0           # OpenHands loop counter
```

---

## PM AGENT OUTPUT

```python
class Feature(BaseModel):
    name: str
    description: str
    priority: Literal["must_have","should_have","nice_to_have"]
    acceptance_criteria: list[str]

class PRDSchema(BaseModel):
    version: str = "1.0"
    project_name: str
    one_liner: str                       # max 120 chars
    target_users: str
    core_features: list[Feature]
    out_of_scope: list[str]
    success_metrics: list[str]
    tech_constraints: list[str]          # from brand memory + Knowledge Graph
    acceptance_criteria: list[str]
    estimated_complexity: Literal["simple","medium","complex"]
    estimated_credits: int               # FinOps pre-check
    skill_hints: list[str]               # suggested skill names for Architect
```

---

## ARCHITECT AGENT OUTPUT

```python
class DataModel(BaseModel):
    name: str
    fields: dict[str, str]              # field_name → type
    relationships: list[str]
    supabase_rls_policy: str | None     # Row Level Security

class APIRoute(BaseModel):
    method: Literal["GET","POST","PUT","DELETE","PATCH"]
    path: str
    description: str
    auth_required: bool
    request_body: dict | None
    response_schema: dict

class TechSpecSchema(BaseModel):
    version: str = "1.0"
    stack: dict = {"frontend": "Next.js 15","backend": "Supabase","deploy": "Vercel"}
    data_models: list[DataModel]
    api_routes: list[APIRoute]
    component_tree: dict
    env_vars_needed: list[str]
    third_party_integrations: list[str]
    estimated_files: int
    supabase_schema_sql: str            # complete migration SQL
    agent_task_breakdown: dict[str, list[str]]  # agent → tasks
    skill_assignments: dict[str, str]   # task_name → skill_file
```

---

## DESIGN AGENT OUTPUT

```python
class DesignToken(BaseModel):
    colors: dict[str, str]             # name → hex
    spacing: dict[str, str]            # name → px value
    typography: dict[str, dict]        # style_name → {size, weight, family}
    radii: dict[str, str]              # name → px
    shadows: dict[str, str]

class WireframeSchema(BaseModel):
    version: str = "1.0"
    mode: Literal["figma","screenshot","prd_only"]
    design_tokens: DesignToken         # exact values — no guessing
    component_list: list[str]          # ordered list of components to build
    layout_description: str            # flex/grid pattern
    visual_similarity_score: float | None  # if screenshot mode
    figma_file_key: str | None
    spec_document: str                 # full extracted spec (screenshot mode)
```

---

## SECURITY AGENT OUTPUT

```python
class SecurityFinding(BaseModel):
    severity: Literal["critical","high","medium","low","info"]
    rule_id: str
    file_path: str
    line_number: int
    description: str
    remediation: str
    owasp_category: str | None

class SecurityReport(BaseModel):
    version: str = "1.0"
    verdict: Literal["PASS","FAIL"]
    critical_count: int
    high_count: int
    findings: list[SecurityFinding]
    owasp_checks_passed: list[str]
    owasp_checks_failed: list[str]
    snyk_report_url: str | None
    semgrep_rules_run: int
    # FAIL if ANY critical or high findings
```

---

## TESTING AGENT OUTPUT

```python
class TestCase(BaseModel):
    name: str
    type: Literal["unit","integration","e2e"]
    status: Literal["passed","failed","skipped"]
    duration_ms: int
    error_message: str | None

class TestResults(BaseModel):
    version: str = "1.0"
    verdict: Literal["PASS","FAIL"]
    total_tests: int
    passed: int
    failed: int
    skipped: int
    coverage_percent: float
    test_cases: list[TestCase]
    e2b_session_id: str
    iterations_needed: int             # how many LoopAgent iterations
```

---

## CRITIC AGENT OUTPUT

```python
class CriticVerdict(BaseModel):
    version: str = "1.0"
    verdict: Literal["APPROVE","REJECT"]
    confidence: float                  # 0.0 to 1.0
    summary: str                       # max 200 words — shown in HITL gate
    issues: list[str]                  # if REJECT
    risk_level: Literal["low","medium","high"]
    rollback_plan: str
    estimated_deploy_time_mins: int
```

---

## HITL GATE PAYLOAD

```python
class HITLPayload(BaseModel):
    project_id: str
    project_name: str
    critic_summary: str                # plain English, max 200 words
    risk_level: str
    files_changed: list[str]
    lines_added: int
    lines_removed: int
    git_diff_url: str
    git_commit_sha: str
    security_status: str               # "PASS" or critical findings summary
    test_coverage: float
    rollback_plan: str
    estimated_deploy_time: str
    skills_used: list[str]             # which skills were loaded
    # Human actions: APPROVE / REJECT / STEER / PAUSE
```

---

## SKILL METADATA (Level 1 — always loaded)

```python
class SkillMetadata(BaseModel):
    id: str                            # e.g. "supabase-auth"
    name: str                          # "Supabase Auth — Complete Auth Flow"
    description: str                   # one sentence
    category: str                      # auth/payments/ui/api/deploy/testing
    tags: list[str]
    stack_requirements: list[str]      # ["next.js", "supabase"]
    success_rate: float                # % from Collective Brain
    last_updated: datetime
```

*v2.0 — March 2026*
