# NOW.md — Current Working Context v2.0
> Update at START and END of every session.
> Always answers: "What am I building RIGHT NOW?"

---

## ACTIVE TASK
**Task:** Stage 4 UI buildout — 14-screen React conversion + validation
**Started:** March 2026
**Status:** In progress — all 14 screens converted; Stitch asset ingestion blocked by access/policy
**Priority:** P0 — finalize design fidelity + asset import

---

## CURRENT GOAL
Complete and stabilize the Forge frontend baseline across all target product screens:

```
1. Convert all 14 provided UI specs into Next.js/React routes
2. Keep canonical folder structure untouched while adding missing routes
3. Validate each implementation phase with test runs
4. Stabilize platform configs (`tsconfig`, `next`, `tailwind`, `postcss`)
5. Import Stitch assets/code where accessible
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
- Converted 14 Forge screens into React/Next routes across `(marketing)` and `(app)` groups
- Added shared UI shell components (`forge-chrome`, `forge-screen`) and global design tokens
- Added missing app routes: marketplace, laboratory, teammate deep-dive, success report, terminal
- Ran staged validation after each phase (`11 passed` each run)
- Restored broken `platform` config files (`package.json`, `tsconfig.json`, `next.config.ts`, `tailwind.config.ts`, `postcss.config.js`, `next-env.d.ts`)
- Confirmed remaining blocker: Stitch project URLs are not retrievable in this environment without an accessible export path

**Next step:** ingest Stitch exports (or user-provided hosted artifacts), then do per-screen fidelity pass and e2e checks

---

## CONTEXT TO CARRY FORWARD
- Agent runtime = OpenHands-style loop: observe() → think() → act() → repeat
- Each agent runs in its OWN E2B sandbox with purpose-specific Docker image
- Agents communicate ONLY via LangGraph state — never directly
- Skills use progressive disclosure: L1 metadata always loaded (~100 tokens each), L2 on trigger, L3 on demand
- Screenshot→code uses 2-pass: Gemini vision extracts spec → Claude builds → visual verify ≥88%
- Google ADK handles: Parallel (frontend∥backend), Loop (testing retry), Resume (HITL), A2A (dynamic spawn)

*v2.0 — March 2026*
