# NOW.md — Current Working Context v2.0
> Update at START and END of every session.
> Always answers: "What am I building RIGHT NOW?"

---

## ACTIVE TASK
**Task:** Core Loop stage hardening — Stage 1 through Stage 10 test/commit execution
**Started:** March 2026
**Status:** Completed in this session — all stage suites passing with per-stage commits
**Priority:** P0 — continue implementation depth in non-scaffold agents while preserving green regression

---

## CURRENT GOAL
Stabilize the end-to-end Forge pipeline scaffolds and keep stage gates continuously green:

```
1. Keep Stage 1-10 integration + unit suites passing on every change
2. Preserve HITL gate behavior before any deploy action
3. Maintain per-stage commit cadence for traceability
4. Expand scaffold agents incrementally to real provider-backed behavior
5. Keep memory docs in sync after each implementation wave
```

---

## CURRENT SPRINT FILES TO CREATE
```
forge/
  core/
    state.py          ← ForgeState Pydantic model ✅
    graph.py          ← LangGraph StateGraph definition ✅ (routing hook added)
    runtime.py        ← AgentRuntime (E2B sandbox wrapper)
  agents/
    base.py           ← BaseAgent OpenHands loop ✅
    pm_agent.py       ← PM Agent (text → PRDSchema) ✅ improved
    architect.py      ← Architect Agent (PRD → TechSpecSchema) ✅ improved
    frontend.py       ← Frontend Agent (Gemini 3 Pro + v0.dev)
    backend.py        ← Backend Agent (Claude Sonnet)
    finops.py         ← FinOps Agent (token budget enforcement)
    critic.py         ← Critic Agent (final quality gate)
  skills/
    loader.py         ← Progressive disclosure skill loader
  sandbox/
    e2b_runtime.py    ← E2B sandbox per-agent runtime
  hitl/
    gate.py           ← HITL approval gate (ADK Resume pattern)
```

---

## ARCHITECTURE DECISIONS AFFECTING THIS SPRINT
- **LangGraph** owns master ForgeState graph
- **Google ADK** ParallelAgent for Frontend ∥ Backend ∥ Design
- **Google ADK** LoopAgent for Testing Agent retry loop
- **Google ADK** Resume for HITL gate pause/resume
- **A2A protocol** for dynamic agent spawning (Spawn Engine)
- **E2B sandbox per agent** — each agent gets own runtime image
- **Git as artifact transport** — agents commit, next agent pulls
- **Progressive disclosure** for Skills — load metadata only at startup

---

## PYDANTIC STATE SCHEMA (agreed, build this first)
```python
class ForgeState(BaseModel):
    # Identity
    project_id: str
    user_id: str
    session_id: str
    created_at: datetime

    # Input
    user_input: str

    # Agent outputs
    prd: PRDSchema | None = None
    tech_spec: TechSpecSchema | None = None
    wireframes: WireframeSchema | None = None
    frontend_code: dict | None = None
    backend_code: dict | None = None
    security_report: SecurityReport | None = None
    test_results: TestResults | None = None
    critic_verdict: CriticVerdict | None = None

    # HITL
    hitl_status: Literal["not_started","pending","approved","rejected"] = "not_started"
    hitl_approval_token: str | None = None

    # Operations
    token_budget: TokenBudget
    errors: list[AgentError] = []
    pipeline_status: Literal["running","paused","completed","failed"] = "running"
    current_agent: str | None = None
    skill_used: str | None = None  # which SKILL.md was loaded
```

---

## LAST SESSION SUMMARY
**Date:** March 2026
**What we did:**
- Replaced placeholder tests for Stage 1, Stage 2, full pipeline, state, HITL, FinOps, and knowledge graph coverage
- Fixed pipeline control flow so rebuild-required outcomes still pause at HITL gate
- Executed stage-by-stage validation and committed each phase checkpoint
- Verified Stage 1-10 coverage via targeted suites and finished with full regression
- Current status: `23 passed` (`pytest -q`) on the full test suite

**Next step:** implement deeper non-scaffold agent behavior (provider-backed PM/Architect/Build/Quality) while preserving stage test contracts

---

## CONTEXT TO CARRY FORWARD
- Agent runtime = OpenHands-style loop: observe() → think() → act() → repeat
- Each agent runs in its OWN E2B sandbox with purpose-specific Docker image
- Agents communicate ONLY via LangGraph state — never directly
- Skills use progressive disclosure: L1 metadata always loaded (~100 tokens each), L2 on trigger, L3 on demand
- Screenshot→code uses 2-pass: Gemini vision extracts spec → Claude builds → visual verify ≥88%
- Google ADK handles: Parallel (frontend∥backend), Loop (testing retry), Resume (HITL), A2A (dynamic spawn)

*v2.0 — March 2026*
