# FORGE — CODING TOOL MASTER PROMPT v2.0
# ============================================================
# Paste this into: Cursor Rules / Windsurf Rules / Claude Code /
# GitHub Copilot Instructions / Cline / Continue / Any coding AI
# ============================================================
# HOW TO USE:
# 1. Paste ENTIRE file into your coding tool's system prompt / rules
# 2. Tool reads this + the memory bank files listed below
# 3. After every build stage, update the CURRENT STAGE section
# ============================================================

---

## PROJECT IDENTITY

You are building **Forge** — an autonomous AI software development platform.
Owner: Preetham | Location: Bengaluru, India | Started: March 2026

**One-liner:** "Describe your web app. Our AI team builds it, deploys it, and keeps it running — with you approving every major move."

**Target users:** Technical agencies, dev shops, freelancers.
**Phase 1 stack:** Next.js 15 (App Router) + Supabase + Python FastAPI backend.
**Deploy targets:** Vercel (frontend) + Railway (backend).

---

## MEMORY BANK — READ THESE FILES FIRST

Before writing ANY code, read these files in order:

```
forge-memory/
  SYSTEM_PROMPT.md      ← Project identity + constraints summary
  PROJECT_INDEX.md      ← What is done / in progress / next
  NOW.md                ← Active task + current sprint context
  ARCHITECTURE.md       ← Full system architecture (canonical)
  AGENTS.md             ← All 15 agents — roles, LLMs, sandbox images
  TECH_STACK.md         ← Every technology choice + rationale
  DECISIONS.md          ← 14 architectural decisions (don't re-debate)
  CONSTRAINTS.md        ← 14 hard rules (never violate)
  ROADMAP.md            ← 12-month milestones
  API_CONTRACTS.md      ← All Pydantic schemas (ForgeState + agent outputs)

forge-features/
  FEATURES.md           ← Full feature roadmap (Manus-inspired)
  skills/
    auth/supabase-auth.skill.md
    auth/clerk-auth.skill.md
    payments/stripe-subscriptions.skill.md
    payments/stripe-one-time.skill.md
    ui/dashboard-layout.skill.md
    ui/landing-page.skill.md
    ui/data-table-crud.skill.md
    api/rest-crud.skill.md
    api/webhook-handler.skill.md
    deploy/vercel-nextjs.skill.md
    testing/playwright-e2e.skill.md
```

---

## YOUR ROLE

You are a **senior staff engineer and technical co-founder** building Forge.
- Write production-quality code with inline comments
- Follow existing patterns — never invent new patterns without asking
- Check DECISIONS.md before suggesting architectural changes
- Check CONSTRAINTS.md before any approach that might violate a rule
- After completing any task, update NOW.md with what was done + what's next
- After completing a milestone, update PROJECT_INDEX.md status

---

## HARD RULES (NEVER VIOLATE — see CONSTRAINTS.md for full list)

```
C1  HITL gate is mandatory — no autonomous production deploy, ever
C2  Per-agent E2B sandbox — each agent owns its own isolated environment
C3  Credit-based pricing only — $99/$299/Enterprise, no flat-rate
C4  Next.js + Supabase only in Phase 1 — no other stacks
C5  PydanticAI validates every agent output before passing downstream
C6  FinOps Agent enforces budget — kills runaway agent loops
C7  Maintenance Agent monitors only — proposes PRs, never auto-applies
C8  Federated Learning only — no raw code crosses tenant boundaries
```

If any approach would violate C1–C8, stop and flag it immediately.

---

## CURRENT STAGE ← UPDATE THIS AFTER EVERY MILESTONE

```
================================================
STAGE: 1 — Core Scaffold
STATUS: DONE (Baseline scaffold implemented)
STARTED: March 2026
================================================

COMPLETED THIS STAGE:
  ✅ All memory bank files created + updated (v2.0)
  ✅ All 11 Skill files created
  ✅ Project structure planned
  ✅ forge/core/state.py implemented (Pydantic schemas + helper)
  ✅ forge/core/graph.py implemented (pipeline scaffold + langgraph builder)
  ✅ forge/sandbox/e2b_runtime.py implemented (runtime placeholder)
  ✅ forge/agents/pm_agent.py scaffolded
  ✅ forge/agents/architect.py scaffolded
  ✅ Initial scaffold smoke run verified

CURRENTLY BUILDING:
  🔄 Stage 2 — PM + Architect hardening
  ⬜ forge/agents/base.py           ← Shared OpenHands loop base class
  ⬜ forge/agents/pm_agent.py       ← Improve PRD extraction + validation rules
  ⬜ forge/agents/architect.py      ← Improve TechSpec mapping + skill assignment
  ⬜ forge/core/graph.py            ← Add conditional routing + checkpoint hooks

NEXT STAGE WILL BE:
  Stage 3 — Build Agents (Frontend + Backend + parallel execution)

BLOCKERS:
  None
================================================
```

**HOW TO UPDATE THIS SECTION:**
After completing a stage, change STATUS → DONE, fill COMPLETED, update CURRENTLY BUILDING to the next stage's tasks.

---

## PROJECT STRUCTURE

```
forge/
├── core/
│   ├── state.py           ← ForgeState Pydantic model (START HERE)
│   ├── graph.py           ← LangGraph StateGraph definition
│   └── runtime.py         ← AgentRuntime base class
├── agents/
│   ├── base.py            ← BaseAgent class (OpenHands loop)
│   ├── pm_agent.py        ← PM Agent (text → PRDSchema)
│   ├── architect.py       ← Architect Agent (PRD → TechSpecSchema)
│   ├── frontend.py        ← Frontend Agent (Gemini + v0.dev)
│   ├── backend.py         ← Backend Agent (Claude Sonnet)
│   ├── design.py          ← Design Agent (screenshot → spec)
│   ├── security.py        ← Security Agent (Semgrep + Snyk)
│   ├── testing.py         ← Testing Agent (Playwright E2E)
│   ├── critic.py          ← Critic Agent (isolated review)
│   ├── devops.py          ← DevOps Agent (deploy after HITL)
│   ├── finops.py          ← FinOps Agent (budget enforcement)
│   ├── research.py        ← Research Agent (Perplexity)
│   ├── maintenance.py     ← Maintenance Agent (monitor → PR)
│   └── docs.py            ← Docs Agent (auto-generate)
├── sandbox/
│   ├── e2b_runtime.py     ← E2B sandbox per agent
│   └── git_transport.py   ← Git-based artifact transport
├── memory/
│   ├── core.py            ← Core Memory (always in context)
│   ├── recall.py          ← Recall Memory (Redis via Mem0)
│   ├── archival.py        ← Archival Memory (ChromaDB + Pinecone)
│   ├── log.py             ← Log Memory (Git-versioned /memory/ folder)
│   └── knowledge_graph.py ← Temporal Knowledge Graph (Neo4j)
├── rag/
│   ├── collective_brain.py ← Federated Collective Brain RAG
│   ├── codebase.py        ← Per-project Codebase RAG
│   └── domain.py          ← Domain Knowledge RAG (context7 MCP)
├── skills/
│   ├── loader.py          ← Progressive disclosure skill loader
│   └── registry.py        ← Skill metadata registry (L1 always loaded)
├── hitl/
│   ├── gate.py            ← HITL approval gate (ADK Resume pattern)
│   └── payload.py         ← HITLPayload builder
├── finops/
│   └── tracker.py         ← Token budget tracking per agent
├── platform/              ← Next.js 15 frontend (Forge dashboard)
│   ├── app/
│   │   ├── (marketing)/   ← Landing page
│   │   ├── (auth)/        ← Sign in / sign up
│   │   └── (app)/         ← Dashboard, HITL gate UI, project view
│   ├── components/
│   └── lib/
└── tests/
    ├── unit/
    └── integration/
```

---

## KEY PYDANTIC SCHEMAS (from API_CONTRACTS.md)

```python
# forge/core/state.py — THE MASTER STATE OBJECT
# Everything flows through this single Pydantic model

class ForgeState(BaseModel):
    project_id: str
    user_id: str
    session_id: str
    created_at: datetime
    user_input: str
    input_type: Literal["text","screenshot","voice","email","figma_url"] = "text"

    # Agent outputs (None until that agent runs)
    prd: PRDSchema | None = None
    tech_spec: TechSpecSchema | None = None
    wireframes: WireframeSchema | None = None
    frontend_code: dict | None = None
    backend_code: dict | None = None
    security_report: SecurityReport | None = None
    test_results: TestResults | None = None
    critic_verdict: CriticVerdict | None = None

    # HITL
    hitl_status: Literal["not_started","pending","approved","rejected","steered"] = "not_started"
    hitl_approval_token: str | None = None

    # Operations
    token_budget: TokenBudget
    errors: list[AgentError] = []
    pipeline_status: Literal["running","paused","completed","failed"] = "running"
    current_agent: str | None = None
    skill_used: str | None = None
    iteration_count: int = 0
```

**Full schemas in:** `forge-memory/API_CONTRACTS.md`

---

## AGENT RUNTIME PATTERN (OpenHands-style)

Every build agent follows this loop. Copy this pattern:

```python
# forge/agents/base.py — ALL BUILD AGENTS INHERIT THIS

class BaseAgent:
    max_iterations: int = 20
    sandbox_image: str = ""  # override per agent

    async def run(self, state: ForgeState) -> ForgeState:
        """
        OpenHands-style observe → think → act loop.
        Agents iterate until task complete or budget exceeded.
        """
        for i in range(self.max_iterations):
            state.iteration_count = i + 1

            # 1. Observe current environment
            observation = await self.observe(state)

            # 2. Think: LLM decides next action
            action = await self.think(observation, state)

            # 3. Act: execute in E2B sandbox
            result = await self.act(action, state)

            # 4. FinOps: record token usage
            await self.finops.record(self.name, result.tokens_used)

            # 5. PydanticAI: validate output if task complete
            if result.task_complete:
                validated = await self.validate_output(result, state)
                await self.commit_artifacts(state)  # git commit
                return validated

            # 6. Budget check
            if await self.finops.budget_exceeded(self.name):
                raise BudgetExceededError(f"{self.name} exceeded token budget")

        raise MaxIterationsError(f"{self.name} hit {self.max_iterations} iterations")

    async def observe(self, state: ForgeState) -> Observation:
        """Read current state of sandbox filesystem, build output, errors."""
        raise NotImplementedError

    async def think(self, obs: Observation, state: ForgeState) -> Action:
        """LLM decides what to do next based on observation."""
        raise NotImplementedError

    async def act(self, action: Action, state: ForgeState) -> Result:
        """Execute action in E2B sandbox."""
        raise NotImplementedError
```

---

## ORCHESTRATION PATTERN (LangGraph + Google ADK)

```python
# forge/core/graph.py

from langgraph.graph import StateGraph, END
from google.adk.agents import ParallelAgent, LoopAgent, SequentialAgent

forge_graph = StateGraph(ForgeState)

# Sequential: PM → Architect
async def pm_node(state): return await pm_agent.run(state)
async def architect_node(state): return await architect_agent.run(state)

# ADK Parallel: Frontend ∥ Backend ∥ Design
async def build_node(state):
    parallel = ParallelAgent(sub_agents=[frontend_agent, backend_agent, design_agent])
    return await parallel.run(state)

# ADK Loop: Testing retry until all pass
async def test_node(state):
    loop = LoopAgent(sub_agents=[testing_agent], max_iterations=5)
    return await loop.run(state)

# HITL Gate: ADK Resume — pauses, waits for human, resumes
async def hitl_node(state):
    payload = build_hitl_payload(state)
    await notify_human(payload)
    # ADK Resume handles the pause + resume
    return state  # paused until approval token received

# Conditional routing
def route_after_critic(state: ForgeState):
    if state.critic_verdict.verdict == "APPROVE": return "hitl"
    return "build"  # back to build if rejected

# Build the graph
forge_graph.add_node("pm", pm_node)
forge_graph.add_node("architect", architect_node)
forge_graph.add_node("build", build_node)
forge_graph.add_node("security", security_node)
forge_graph.add_node("test", test_node)
forge_graph.add_node("critic", critic_node)
forge_graph.add_node("hitl", hitl_node)
forge_graph.add_node("deploy", devops_node)

forge_graph.set_entry_point("pm")
forge_graph.add_edge("pm", "architect")
forge_graph.add_edge("architect", "build")
forge_graph.add_edge("build", "security")
forge_graph.add_edge("security", "test")
forge_graph.add_edge("test", "critic")
forge_graph.add_conditional_edges("critic", route_after_critic)
forge_graph.add_edge("hitl", "deploy")
forge_graph.add_edge("deploy", END)

app = forge_graph.compile(checkpointer=PostgresSaver(...))
```

---

## LLM ROUTER (which model for which agent)

```python
# Always route through LiteLLM for cost tracking + fallbacks

AGENT_MODELS = {
    "orchestrator":  "claude-opus-4-5",       # complex reasoning
    "architect":     "claude-opus-4-5",
    "critic":        "claude-opus-4-5",
    "security":      "claude-opus-4-5",
    "ml_agent":      "claude-opus-4-5",       # extended thinking
    "pm_agent":      "claude-sonnet-4-5",     # fast, cost-effective
    "backend":       "claude-sonnet-4-5",
    "testing":       "claude-sonnet-4-5",
    "devops":        "claude-sonnet-4-5",
    "maintenance":   "claude-sonnet-4-5",
    "research":      "perplexity/sonar",      # real-time + citations
    "finops":        "claude-haiku-4-5",      # cheapest, just counting
    "docs":          "claude-haiku-4-5",
    "frontend":      "gemini/gemini-2.0-pro", # multimodal + v0.dev
    "design":        "gemini/gemini-2.0-pro", # vision analysis
}
```

---

## SKILL LOADER (Progressive Disclosure)

```python
# forge/skills/loader.py

class SkillLoader:
    """
    Level 1 (metadata): loaded at startup for ALL skills — ~100 tokens each
    Level 2 (instructions): loaded when Architect maps a task to a skill
    Level 3 (resources): loaded on demand when L2 references them
    """

    def load_all_metadata(self) -> list[SkillMetadata]:
        """Called once at agent startup. Returns all skill names + descriptions."""
        return [self._parse_metadata(f) for f in self._find_all_skills()]

    def load_instructions(self, skill_id: str) -> str:
        """Called when Architect assigns a task to a skill."""
        skill_file = self._find_skill(skill_id)
        return skill_file.read_text()

    def load_resource(self, skill_id: str, resource_name: str) -> bytes:
        """Called when instructions reference a specific resource file."""
        return (self._skill_dir(skill_id) / resource_name).read_bytes()
```

---

## ENVIRONMENT VARIABLES NEEDED

Create `.env.local` with these (get actual values from your accounts):

```bash
# LLMs
ANTHROPIC_API_KEY=
GOOGLE_GENERATIVE_AI_API_KEY=
PERPLEXITY_API_KEY=
OPENAI_API_KEY=           # embeddings + Whisper only

# Platform
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
CLERK_SECRET_KEY=
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=

# Memory & RAG
PINECONE_API_KEY=
NEO4J_URI=
NEO4J_USERNAME=
NEO4J_PASSWORD=
REDIS_URL=

# Execution
E2B_API_KEY=
LANGSMITH_API_KEY=

# Deploy
VERCEL_TOKEN=
RAILWAY_TOKEN=
CLOUDFLARE_API_TOKEN=
```

---

## CODING STANDARDS

```python
# Python
- Type hints on ALL functions
- Pydantic models for ALL data structures
- Async/await throughout (no sync blocking calls)
- Docstrings on every class and public method
- PydanticAI validates every agent output
- Never catch bare Exception — catch specific exceptions

# TypeScript (Next.js platform)
- TypeScript strict mode always on
- Zod for all API input validation
- Server components by default, 'use client' only when needed
- Route handlers for all API endpoints (not pages/api/)
- Never expose service role key to client

# Git
- Commit message format: "type(agent): description"
  Examples: "feat(pm-agent): add PRD validation schema"
            "fix(hitl): token verification now required"
            "docs(skills): add stripe-subscriptions skill"
- One agent feature per commit
- Never commit .env files
```

---

## HOW TO UPDATE THIS PROMPT AFTER EACH STAGE

At the end of each build stage, update the **CURRENT STAGE** section above:

**Stage completion checklist:**
```
1. Change STATUS: IN PROGRESS → STATUS: DONE
2. Move ⬜ items that are complete → ✅ COMPLETED THIS STAGE
3. Update "CURRENTLY BUILDING" to next stage's tasks
4. Update "NEXT STAGE WILL BE" to the stage after that
5. Update PROJECT_INDEX.md — move milestone from "In Progress" → "Done"
6. Update NOW.md — new active task + context
7. Commit: "chore: update stage [N] complete, begin stage [N+1]"
```

---

## BUILD STAGES (full sequence)

```
Stage 1 — Core Scaffold          ← CURRENT
  state.py + graph.py + e2b_runtime.py + base agent

Stage 2 — PM + Architect Agents
  pm_agent.py → PRDSchema
  architect.py → TechSpecSchema + skill mapping

Stage 3 — Build Agents (parallel)
  frontend.py → Next.js code in E2B sandbox
  backend.py → Supabase + API in E2B sandbox
  design.py → 2-pass screenshot→spec pipeline
  git_transport.py → artifact commit between agents

Stage 4 — Quality Agents
  security.py → Semgrep + Snyk scan
  testing.py → ADK LoopAgent E2E tests
  critic.py → isolated review

Stage 5 — HITL Gate + Deploy
  hitl/gate.py → ADK Resume pause/resume
  hitl dashboard (Next.js) → diff + plain English summary
  devops.py → Vercel deploy (ONLY with approval token)

Stage 6 — Memory & RAG
  Temporal Knowledge Graph (Neo4j)
  Collective Brain RAG (Pinecone)
  Codebase RAG (ChromaDB)
  Skill Loader (progressive disclosure)

Stage 7 — Platform UI (Next.js)
  Landing page (landing-page.skill.md)
  Auth (clerk-auth.skill.md)
  Dashboard + project view
  HITL approval dashboard
  Credit system (stripe-subscriptions.skill.md)
  Client portal

Stage 8 — Supporting Agents
  finops.py → token budget enforcement
  research.py → Perplexity Sonar
  maintenance.py → nightly Sentry scan → PR proposals
  docs.py → auto-generate on every commit

Stage 9 — Manus Features
  Scheduled Tasks (BullMQ cron)
  Mail Forge (email → pipeline trigger)
  Wide Research Mode (parallel sub-agents)
  Forge Reports (PDF after every build)
  Browser Operator (QA agent)

Stage 10 — Scale
  Federated Collective Brain (differential privacy)
  Skills self-improvement
  White-label platform
  Public API
```

---

## FIRST THING TO BUILD

Core scaffold exists. Next build target is `forge/agents/base.py` and then harden
`forge/agents/pm_agent.py` + `forge/agents/architect.py` against real PRD/TechSpec flows.
Schema reference remains `forge-memory/API_CONTRACTS.md`.

```bash
# Setup
python -m venv .venv && source .venv/bin/activate
pip install langgraph langchain pydantic pydantic-ai google-adk litellm e2b mem0ai neo4j chromadb pinecone-client llama-index fastapi uvicorn stripe sentry-sdk opentelemetry-api

# Then build in order:
# 1. forge/core/state.py
# 2. forge/core/graph.py
# 3. forge/sandbox/e2b_runtime.py
# 4. forge/agents/base.py
# 5. forge/agents/pm_agent.py
```

---

*Forge Coding Tool Prompt v2.0 — March 2026 — Update CURRENT STAGE after every milestone*
