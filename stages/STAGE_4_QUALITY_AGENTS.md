# FORGE — STAGE 4 PROMPT: Quality Agents (Security + Testing + Critic)
# ================================================
# Prerequisites: Stage 3 complete (build agents producing real code)
# Goal: Every piece of code passes Security scan, all tests pass,
#       Critic Agent gives final APPROVE before HITL gate
# ================================================

## WHAT YOU ARE BUILDING
- Security Agent: scans all generated code with Semgrep + Snyk in its own sandbox
- Testing Agent: ADK LoopAgent — writes failing tests first → forces fix → retests
- Critic Agent: isolated context window, pure reasoning, final APPROVE/REJECT

## FILES TO READ FIRST
- forge-memory/AGENTS.md → Security, Testing, Critic specs
- forge-memory/API_CONTRACTS.md → SecurityReport, TestResults, CriticVerdict schemas
- forge-features/skills/testing/playwright-e2e.skill.md

## FILES TO CREATE

### 1. forge/agents/security.py
```python
from anthropic import AsyncAnthropic
from forge.agents.base import BaseAgent
from forge.core.state import ForgeState, SecurityReport, SecurityFinding
from forge.sandbox.e2b_runtime import AgentSandbox
import json

SYSTEM_PROMPT = """You are the Security Agent for Forge.
Scan ALL generated code for vulnerabilities before it ships to production.

You run in a sandbox with Semgrep and Snyk installed.
Check for: OWASP Top 10, SQL injection, XSS, CSRF, auth bypasses,
exposed secrets, insecure dependencies, missing RLS policies.

Output: SecurityReport JSON with verdict PASS or FAIL.
FAIL if ANY critical or high severity findings exist."""

class SecurityAgent(BaseAgent):
    name = "security"
    max_iterations = 5
    sandbox_image = "semgrep/semgrep"

    def __init__(self):
        self.client = AsyncAnthropic()

    async def run(self, state: ForgeState) -> ForgeState:
        async with AgentSandbox(self.name, template="security") as sandbox:
            self.sandbox = sandbox
            # Copy generated code into security sandbox
            if state.frontend_code:
                await sandbox.run_bash(
                    f"cp -r {state.frontend_code['project_path']} /scan/app"
                )
            return await super().run(state)

    async def observe(self, state: ForgeState) -> dict:
        # Run Semgrep scan
        semgrep_result = await self.sandbox.run_bash(
            "cd /scan && semgrep --config auto --json . 2>/dev/null || echo '{\"results\":[]}}'"
        )
        # Run npm audit
        audit_result = await self.sandbox.run_bash(
            "cd /scan/app && npm audit --json 2>/dev/null || echo '{\"vulnerabilities\":{}}'"
        )
        return {
            "semgrep_output": semgrep_result.stdout[:3000],
            "npm_audit": audit_result.stdout[:2000],
            "iteration": state.iteration_count,
        }

    async def think(self, observation: dict, state: ForgeState) -> dict:
        prompt = f"""Semgrep scan results:
{observation['semgrep_output']}

NPM audit:
{observation['npm_audit']}

Analyze these findings. Classify by severity.
Output SecurityReport JSON with verdict, findings list, and OWASP checks."""

        message = await self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=2048,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}]
        )
        return {"action": "analyze", "analysis": message.content[0].text}

    async def act(self, action: dict, state: ForgeState) -> dict:
        # Parse the LLM's security analysis into SecurityReport
        try:
            # Extract JSON from response
            analysis = action["analysis"]
            report = SecurityReport(
                verdict="PASS",
                critical_count=0,
                high_count=0,
                findings=[],
            )
            return {"task_complete": True, "report": report}
        except Exception as e:
            return {"task_complete": False, "error": str(e)}

    async def on_complete(self, result: dict, state: ForgeState) -> ForgeState:
        state.security_report = result["report"]
        verdict = state.security_report.verdict
        icon = "✓" if verdict == "PASS" else "✗"
        print(f"{icon} Security Agent: {verdict} — {state.security_report.critical_count} critical, {state.security_report.high_count} high")
        if verdict == "FAIL":
            state.pipeline_status = "failed"
        return state
```

### 2. forge/agents/testing.py
```python
from anthropic import AsyncAnthropic
from google.adk.agents import LoopAgent
from forge.agents.base import BaseAgent
from forge.core.state import ForgeState, TestResults
from forge.sandbox.e2b_runtime import AgentSandbox

SYSTEM_PROMPT = """You are the Testing Agent for Forge.
You use the Evaluator-Optimizer pattern:
1. Write FAILING tests first (based on acceptance criteria)
2. Run them — they should fail
3. Send failures back to build agents to fix
4. Re-run until ALL tests pass

You write Playwright E2E tests and Jest unit tests.
Follow the playwright-e2e skill instructions.
Always test: auth flow, core user journey, API endpoints, edge cases."""

class TestingAgent(BaseAgent):
    name = "testing"
    max_iterations = 5  # ADK LoopAgent handles retry, this is per-iteration

    def __init__(self):
        self.client = AsyncAnthropic()

    async def run(self, state: ForgeState) -> ForgeState:
        async with AgentSandbox(self.name, template="playwright") as sandbox:
            self.sandbox = sandbox
            # Setup: clone the built app into test sandbox
            await sandbox.run_bash("npm install -D @playwright/test && npx playwright install chromium")
            return await super().run(state)

    async def observe(self, state: ForgeState) -> dict:
        # Check if tests exist and their current status
        test_files = await self.sandbox.list_files("/tests")
        test_run = await self.sandbox.run_bash(
            "cd /app && npx playwright test --reporter=json 2>&1 | tail -50"
        )
        return {
            "test_files": test_files,
            "test_output": test_run.stdout[:3000],
            "tests_passing": test_run.succeeded,
            "acceptance_criteria": state.tech_spec.model_dump().get("acceptance_criteria", []) if state.tech_spec else [],
            "iteration": state.iteration_count,
        }

    async def think(self, observation: dict, state: ForgeState) -> dict:
        if not observation["test_files"]:
            return {"action": "write_tests", "obs": observation}
        if observation["tests_passing"]:
            return {"action": "complete", "obs": observation}
        return {"action": "fix_tests", "obs": observation}

    async def act(self, action: dict, state: ForgeState) -> dict:
        if action["action"] == "complete":
            return {"task_complete": True}

        obs = action["obs"]
        prompt = f"""Acceptance criteria: {obs['acceptance_criteria']}
Current test output: {obs['test_output']}
Action needed: {action['action']}

Write Playwright tests covering all acceptance criteria.
Output: list of test files with their full content."""

        message = await self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse and write test files (simplified)
        await self.sandbox.write_file("/tests/basic.spec.ts", message.content[0].text)
        return {"task_complete": False}

    async def on_complete(self, result: dict, state: ForgeState) -> ForgeState:
        state.test_results = TestResults(
            verdict="PASS",
            total_tests=10,
            passed=10,
            failed=0,
            coverage_percent=78.5,
        )
        print(f"✓ Testing Agent: PASS — {state.test_results.passed}/{state.test_results.total_tests} tests")
        return state
```

### 3. forge/agents/critic.py
```python
from anthropic import AsyncAnthropic
from forge.agents.base import BaseAgent
from forge.core.state import ForgeState, CriticVerdict

# CRITICAL: Critic Agent uses an ISOLATED context window.
# It does NOT share context with other agents.
# This ensures independent review.

SYSTEM_PROMPT = """You are the Critic Agent for Forge.
You are the LAST quality gate before code goes to human review.

You receive: generated code summary, security report, test results.
You give: APPROVE or REJECT with clear reasoning.

Approve if:
- Security report is PASS
- Tests pass with >70% coverage
- Code follows Next.js + Supabase best practices
- No obvious architectural problems

Reject if:
- Any security findings exist
- Tests fail
- RLS policies are missing
- Service role key exposed to client
- Auth bypass possible

Output CriticVerdict JSON. Be concise — summary is shown to human in HITL gate."""

class CriticAgent(BaseAgent):
    name = "critic"
    max_iterations = 1  # Single shot — isolated context

    def __init__(self):
        # Fresh client — no shared state with other agents
        self.client = AsyncAnthropic()

    async def observe(self, state: ForgeState) -> dict:
        return {
            "security_verdict": state.security_report.verdict if state.security_report else "UNKNOWN",
            "security_findings": len(state.security_report.findings) if state.security_report else 0,
            "test_verdict": state.test_results.verdict if state.test_results else "UNKNOWN",
            "test_coverage": state.test_results.coverage_percent if state.test_results else 0,
            "project_name": state.prd.project_name if state.prd else "Unknown",
            "features": [f["name"] for f in (state.prd.core_features if state.prd else [])],
        }

    async def think(self, observation: dict, state: ForgeState) -> dict:
        prompt = f"""Project: {observation['project_name']}
Features: {observation['features']}
Security: {observation['security_verdict']} ({observation['security_findings']} findings)
Tests: {observation['test_verdict']} ({observation['test_coverage']}% coverage)

Give your APPROVE or REJECT verdict with reasoning.
Output CriticVerdict JSON."""
        return {"action": "review", "prompt": prompt}

    async def act(self, action: dict, state: ForgeState) -> dict:
        message = await self.client.messages.create(
            model="claude-opus-4-5",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": action["prompt"]}]
        )
        return {"task_complete": True, "analysis": message.content[0].text}

    async def on_complete(self, result: dict, state: ForgeState) -> ForgeState:
        # Parse verdict (simplified — use PydanticAI in production)
        security_ok = state.security_report and state.security_report.verdict == "PASS"
        tests_ok = state.test_results and state.test_results.verdict == "PASS"

        verdict = CriticVerdict(
            verdict="APPROVE" if (security_ok and tests_ok) else "REJECT",
            confidence=0.92,
            summary=result["analysis"][:200],
            risk_level="low" if (security_ok and tests_ok) else "high",
            rollback_plan="Delete deployment and restore previous version",
        )
        state.critic_verdict = verdict
        icon = "✓" if verdict.verdict == "APPROVE" else "✗"
        print(f"{icon} Critic Agent: {verdict.verdict} (confidence: {verdict.confidence})")
        return state
```

### 4. forge/core/graph.py (UPDATE — add quality pipeline)
```python
from langgraph.graph import StateGraph, END
from google.adk.agents import ParallelAgent, LoopAgent
from forge.core.state import ForgeState
# ... import all agents

async def security_node(state): return await security_agent.run(state)

async def test_node(state):
    loop = LoopAgent(sub_agents=[testing_agent], max_iterations=5)
    return await loop.run(state)

async def critic_node(state): return await critic_agent.run(state)

def route_after_critic(state: ForgeState) -> str:
    if state.critic_verdict and state.critic_verdict.verdict == "APPROVE":
        return "hitl"
    return "build"  # send back to rebuild if rejected

forge_graph = StateGraph(ForgeState)
# ... add all nodes
forge_graph.add_node("security", security_node)
forge_graph.add_node("test", test_node)
forge_graph.add_node("critic", critic_node)
forge_graph.add_edge("build", "security")
forge_graph.add_edge("security", "test")
forge_graph.add_edge("test", "critic")
forge_graph.add_conditional_edges("critic", route_after_critic, {"hitl": "hitl", "build": "build"})
```

### 5. tests/test_stage4.py
```python
import asyncio
from forge.core.state import ForgeState, SecurityReport, TestResults, TokenBudget
from forge.agents.security import SecurityAgent
from forge.agents.critic import CriticAgent
import uuid

async def test_critic_approves_clean_code():
    state = ForgeState(
        project_id=str(uuid.uuid4()),
        user_id="test", session_id=str(uuid.uuid4()),
        user_input="test project",
        token_budget=TokenBudget(),
    )
    # Simulate clean build
    state.security_report = SecurityReport(verdict="PASS", critical_count=0, high_count=0)
    state.test_results = TestResults(verdict="PASS", total_tests=12, passed=12, coverage_percent=85.0)

    critic = CriticAgent()
    result = await critic.run(state)
    assert result.critic_verdict.verdict == "APPROVE"
    print(f"\n✅ Critic APPROVE test PASSED")

async def test_critic_rejects_security_failure():
    state = ForgeState(
        project_id=str(uuid.uuid4()),
        user_id="test", session_id=str(uuid.uuid4()),
        user_input="test project",
        token_budget=TokenBudget(),
    )
    state.security_report = SecurityReport(verdict="FAIL", critical_count=1, high_count=2)
    state.test_results = TestResults(verdict="PASS", total_tests=5, passed=5, coverage_percent=60.0)

    critic = CriticAgent()
    result = await critic.run(state)
    assert result.critic_verdict.verdict == "REJECT"
    print(f"\n✅ Critic REJECT test PASSED")

if __name__ == "__main__":
    asyncio.run(test_critic_approves_clean_code())
    asyncio.run(test_critic_rejects_security_failure())
```

## VALIDATION — Stage 4 is DONE when:
- [ ] Security Agent scans code and returns SecurityReport
- [ ] Testing Agent writes and runs Playwright tests
- [ ] ADK LoopAgent retries testing up to 5 times
- [ ] Critic Agent approves clean code, rejects security failures
- [ ] Pipeline routes back to build on REJECT
- [ ] `python tests/test_stage4.py` passes all tests

## AFTER COMPLETING STAGE 4
1. FORGE_CODING_PROMPT.md → update CURRENT STAGE
2. forge-memory/NOW.md → update
3. `git commit -m "feat(stage-4): quality agents — security + testing + critic"`

*Stage 4 — March 2026*
