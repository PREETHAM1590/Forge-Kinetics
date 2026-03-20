# FORGE — STAGE 1 PROMPT: Core Scaffold
# ================================================
# Paste this into Cursor / Claude Code / Windsurf / Cline
# when starting Stage 1.
# ================================================

## WHAT YOU ARE BUILDING
You are building the foundational scaffold for Forge — an autonomous AI
software development platform. This stage creates the core Pydantic state
model, LangGraph graph, and per-agent E2B sandbox runtime that every
other stage depends on.

## FILES TO READ FIRST
- forge-memory/ARCHITECTURE.md → system design
- forge-memory/API_CONTRACTS.md → all Pydantic schemas
- forge-memory/CONSTRAINTS.md → hard rules

## STAGE 1 GOAL
Create a working pipeline that runs: input → PM Agent stub → Architect stub
→ HITL stub → deploy stub, with ForgeState flowing through the entire graph.
No real LLM calls yet — use stubs that return mock data so the graph runs
end-to-end first.

## FILES TO CREATE (in this exact order)

### 1. forge/core/state.py
The master Pydantic model. Every agent reads/writes this.
```python
from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

class TokenBudget(BaseModel):
    total_allocated: int = 500_000
    total_used: int = 0
    per_agent: dict[str, int] = Field(default_factory=dict)
    is_exceeded: bool = False

class AgentError(BaseModel):
    agent_name: str
    error_type: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    retry_count: int = 0

class PRDSchema(BaseModel):
    version: str = "1.0"
    project_name: str
    one_liner: str
    target_users: str
    core_features: list[dict]
    out_of_scope: list[str] = []
    acceptance_criteria: list[str] = []
    estimated_complexity: Literal["simple", "medium", "complex"] = "medium"
    estimated_credits: int = 100
    skill_hints: list[str] = []

class TechSpecSchema(BaseModel):
    version: str = "1.0"
    stack: dict = {"frontend": "Next.js 15", "backend": "Supabase", "deploy": "Vercel"}
    data_models: list[dict] = []
    api_routes: list[dict] = []
    component_tree: dict = {}
    env_vars_needed: list[str] = []
    supabase_schema_sql: str = ""
    agent_task_breakdown: dict[str, list[str]] = {}
    skill_assignments: dict[str, str] = {}

class SecurityReport(BaseModel):
    verdict: Literal["PASS", "FAIL"] = "PASS"
    critical_count: int = 0
    high_count: int = 0
    findings: list[dict] = []

class TestResults(BaseModel):
    verdict: Literal["PASS", "FAIL"] = "PASS"
    total_tests: int = 0
    passed: int = 0
    failed: int = 0
    coverage_percent: float = 0.0

class CriticVerdict(BaseModel):
    verdict: Literal["APPROVE", "REJECT"] = "APPROVE"
    confidence: float = 0.9
    summary: str = ""
    issues: list[str] = []
    risk_level: Literal["low", "medium", "high"] = "low"
    rollback_plan: str = ""

class ForgeState(BaseModel):
    # Identity
    project_id: str
    user_id: str
    session_id: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Input
    user_input: str
    input_type: Literal["text","screenshot","voice","email","figma_url"] = "text"

    # Agent outputs
    prd: PRDSchema | None = None
    tech_spec: TechSpecSchema | None = None
    frontend_code: dict | None = None
    backend_code: dict | None = None
    security_report: SecurityReport | None = None
    test_results: TestResults | None = None
    critic_verdict: CriticVerdict | None = None

    # HITL
    hitl_status: Literal["not_started","pending","approved","rejected"] = "not_started"
    hitl_approval_token: str | None = None

    # Operations
    token_budget: TokenBudget = Field(default_factory=TokenBudget)
    errors: list[AgentError] = Field(default_factory=list)
    pipeline_status: Literal["running","paused","completed","failed"] = "running"
    current_agent: str | None = None
    skill_used: str | None = None
    iteration_count: int = 0
```

### 2. forge/agents/base.py
Base agent with OpenHands-style observe→think→act loop.
```python
from abc import ABC, abstractmethod
from forge.core.state import ForgeState, AgentError
from datetime import datetime
import asyncio

class BaseAgent(ABC):
    name: str = "base"
    max_iterations: int = 20
    sandbox_image: str = ""

    async def run(self, state: ForgeState) -> ForgeState:
        """OpenHands-style observe→think→act loop."""
        state.current_agent = self.name
        for i in range(self.max_iterations):
            state.iteration_count = i + 1
            try:
                observation = await self.observe(state)
                action = await self.think(observation, state)
                result = await self.act(action, state)
                if result.get("task_complete"):
                    state = await self.on_complete(result, state)
                    return state
            except Exception as e:
                state.errors.append(AgentError(
                    agent_name=self.name,
                    error_type=type(e).__name__,
                    message=str(e),
                    retry_count=i
                ))
                if i == self.max_iterations - 1:
                    state.pipeline_status = "failed"
                    raise
        return state

    @abstractmethod
    async def observe(self, state: ForgeState) -> dict: ...

    @abstractmethod
    async def think(self, observation: dict, state: ForgeState) -> dict: ...

    @abstractmethod
    async def act(self, action: dict, state: ForgeState) -> dict: ...

    async def on_complete(self, result: dict, state: ForgeState) -> ForgeState:
        """Override to set agent-specific output on state."""
        return state
```

### 3. forge/core/graph.py
LangGraph StateGraph wiring all agents together.
```python
from langgraph.graph import StateGraph, END
from forge.core.state import ForgeState
from forge.agents.pm_agent import PMAgent
from forge.agents.architect import ArchitectAgent

pm_agent = PMAgent()
architect_agent = ArchitectAgent()

async def pm_node(state: ForgeState) -> ForgeState:
    return await pm_agent.run(state)

async def architect_node(state: ForgeState) -> ForgeState:
    return await architect_agent.run(state)

async def hitl_node(state: ForgeState) -> ForgeState:
    """HITL gate — pauses pipeline for human approval."""
    state.hitl_status = "pending"
    state.pipeline_status = "paused"
    print(f"\n=== HITL GATE ===")
    print(f"Project: {state.prd.project_name if state.prd else 'Unknown'}")
    print(f"Risk: {state.critic_verdict.risk_level if state.critic_verdict else 'low'}")
    print(f"Awaiting approval token...")
    return state

def route_after_hitl(state: ForgeState) -> str:
    if state.hitl_status == "approved":
        return "deploy"
    return END

forge_graph = StateGraph(ForgeState)
forge_graph.add_node("pm", pm_node)
forge_graph.add_node("architect", architect_node)
forge_graph.add_node("hitl", hitl_node)
forge_graph.set_entry_point("pm")
forge_graph.add_edge("pm", "architect")
forge_graph.add_edge("architect", "hitl")
forge_graph.add_conditional_edges("hitl", route_after_hitl)
app = forge_graph.compile()
```

### 4. forge/agents/pm_agent.py
PM Agent stub — returns a mock PRD for now.
```python
from forge.agents.base import BaseAgent
from forge.core.state import ForgeState, PRDSchema

class PMAgent(BaseAgent):
    name = "pm_agent"
    max_iterations = 1  # PM Agent is single-shot

    async def observe(self, state: ForgeState) -> dict:
        return {"user_input": state.user_input, "input_type": state.input_type}

    async def think(self, observation: dict, state: ForgeState) -> dict:
        # TODO Stage 2: Replace with real Claude Sonnet call
        return {"action": "generate_prd", "input": observation["user_input"]}

    async def act(self, action: dict, state: ForgeState) -> dict:
        # STUB: Replace with real LLM call in Stage 2
        prd = PRDSchema(
            project_name="Test Project",
            one_liner=f"App for: {action['input'][:80]}",
            target_users="Technical users",
            core_features=[{"name": "Core feature", "description": action["input"]}],
            estimated_complexity="medium",
        )
        return {"task_complete": True, "prd": prd}

    async def on_complete(self, result: dict, state: ForgeState) -> ForgeState:
        state.prd = result["prd"]
        print(f"✓ PM Agent: PRD created — {state.prd.project_name}")
        return state
```

### 5. forge/agents/architect.py
Architect Agent stub — returns a mock TechSpec.
```python
from forge.agents.base import BaseAgent
from forge.core.state import ForgeState, TechSpecSchema

class ArchitectAgent(BaseAgent):
    name = "architect"
    max_iterations = 1

    async def observe(self, state: ForgeState) -> dict:
        return {"prd": state.prd}

    async def think(self, observation: dict, state: ForgeState) -> dict:
        return {"action": "generate_tech_spec", "prd": observation["prd"]}

    async def act(self, action: dict, state: ForgeState) -> dict:
        prd = action["prd"]
        spec = TechSpecSchema(
            data_models=[{"name": "User", "fields": {"id": "uuid", "email": "text"}}],
            api_routes=[{"method": "GET", "path": "/api/health", "auth_required": False}],
            env_vars_needed=["NEXT_PUBLIC_SUPABASE_URL", "SUPABASE_SERVICE_ROLE_KEY"],
            skill_assignments={"auth": "supabase-auth", "deploy": "vercel-nextjs"},
        )
        return {"task_complete": True, "tech_spec": spec}

    async def on_complete(self, result: dict, state: ForgeState) -> ForgeState:
        state.tech_spec = result["tech_spec"]
        print(f"✓ Architect: TechSpec created — {len(state.tech_spec.api_routes)} routes")
        return state
```

### 6. tests/test_stage1.py
Integration test — run the full graph end-to-end.
```python
import asyncio
import pytest
from forge.core.state import ForgeState, TokenBudget
from forge.core.graph import app
import uuid

async def test_full_pipeline_stub():
    """Test the full graph runs end-to-end with stubs."""
    state = ForgeState(
        project_id=str(uuid.uuid4()),
        user_id="test-user",
        session_id=str(uuid.uuid4()),
        user_input="Build a todo app with auth and Stripe payments",
        token_budget=TokenBudget(total_allocated=1_000_000),
    )
    result = await app.ainvoke(state)
    assert result["prd"] is not None
    assert result["tech_spec"] is not None
    assert result["hitl_status"] == "pending"
    print(f"\n✅ Stage 1 pipeline test PASSED")
    print(f"   PRD: {result['prd']['project_name']}")
    print(f"   Skills assigned: {result['tech_spec']['skill_assignments']}")

if __name__ == "__main__":
    asyncio.run(test_full_pipeline_stub())
```

### 7. requirements.txt
```
langgraph>=0.2.0
langchain>=0.3.0
langsmith>=0.1.0
pydantic>=2.0.0
pydantic-ai>=0.0.1
google-adk>=1.0.0
litellm>=1.0.0
anthropic>=0.30.0
e2b>=0.17.0
mem0ai>=0.1.0
neo4j>=5.0.0
graphiti-core>=0.1.0
chromadb>=0.5.0
pinecone-client>=3.0.0
llama-index>=0.10.0
redis>=5.0.0
fastapi>=0.110.0
uvicorn>=0.29.0
stripe>=9.0.0
sentry-sdk>=2.0.0
opentelemetry-api>=1.24.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
```

## VALIDATION — Stage 1 is DONE when:
- [ ] `python -c "from forge.core.state import ForgeState; print('✓ State OK')"` passes
- [ ] `python -c "from forge.core.graph import app; print('✓ Graph OK')"` passes
- [ ] `python tests/test_stage1.py` runs without errors
- [ ] HITL gate pauses the pipeline at the end
- [ ] All files have type hints and docstrings

## AFTER COMPLETING STAGE 1
Update these files:
1. FORGE_CODING_PROMPT.md → CURRENT STAGE → STATUS: DONE, move to Stage 2
2. forge-memory/NOW.md → update Last Session Summary
3. forge-memory/PROJECT_INDEX.md → check off: ForgeState, LangGraph scaffold, base agent, PM stub, Architect stub
4. Run: `git add . && git commit -m "feat(stage-1): core scaffold complete — ForgeState + LangGraph + agent stubs"`

*Stage 1 — March 2026*
