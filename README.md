# ⬡ FORGE

> Autonomous AI Software Development Platform

"Describe your web app. Our AI team builds it, deploys it, and keeps it running — with you approving every major move."

---

## What is Forge?

Forge is a 15-agent AI platform that acts as a software development agency.
Users describe a web app → specialized AI agents plan, build, deploy, and monitor it.
**Every production deploy requires explicit human approval** (HITL gate — non-negotiable).

**Target:** Technical agencies, dev shops, freelancers in Bengaluru → global.
**Stack (Phase 1):** Next.js 15 + Supabase + Python FastAPI backend.

---

## Quick Start

```bash
# 1. Clone and setup
git clone https://github.com/preetham/forge.git
cd forge

# 2. Start local services + install dependencies
chmod +x scripts/setup.sh
./scripts/setup.sh

# 3. Fill in API keys
cp .env.example .env.local
# Edit .env.local with your: ANTHROPIC_API_KEY, E2B_API_KEY, etc.

# 4. Start the API
source .venv/bin/activate
uvicorn forge.api.main:app --reload

# 5. Start the platform
cd platform && npm run dev

# 6. Open http://localhost:3000
```

---

## Memory Bank

All project context lives in `forge-memory/`. Every AI coding tool reads this first.

```
forge-memory/
  SYSTEM_PROMPT.md    ← paste into any AI model to restore full context
  PROJECT_INDEX.md    ← current status + what's done / in progress
  NOW.md              ← active sprint task
  ARCHITECTURE.md     ← canonical system architecture
  AGENTS.md           ← all 15 agents
  TECH_STACK.md       ← every tech choice
  DECISIONS.md        ← 14 architectural decisions
  CONSTRAINTS.md      ← 14 hard rules
  ROADMAP.md          ← 12-month plan
  API_CONTRACTS.md    ← all Pydantic schemas
```

---

## Build Stages

```
Stage 1  → Core scaffold (ForgeState + LangGraph + stubs)
Stage 2  → PM + Architect agents (real Claude calls)
Stage 3  → Frontend + Backend agents (E2B sandboxes)
Stage 4  → Quality agents (Security + Testing + Critic)
Stage 5  → HITL gate + DevOps + Vercel deploy
Stage 6  → Memory + Knowledge Graph + RAG
Stage 7  → Platform UI (Next.js dashboard)
Stage 8  → Supporting agents (FinOps + Maintenance + Docs)
Stage 9  → Manus features (Mail, Wide Research, 2-pass Design)
Stage 10 → Collective Brain + Public API + White-label
```

Current stage: see `FORGE_CODING_PROMPT.md` → CURRENT STAGE section.

---

## Architecture

```
User Input
    │
    ▼
PM Agent → Architect → [Frontend ∥ Backend ∥ Design]
         → Security → Testing (ADK Loop) → Critic
         → HITL Gate (human approval mandatory)
         → DevOps → Deployed App

Always running: FinOps Agent (budget enforcement)
Post-deploy: Maintenance Agent (monitor → PR proposals)
```

**Key decisions:**
- LangGraph + Google ADK hybrid orchestration
- Per-agent E2B sandboxes (OpenHands-style runtime)
- 5-tier memory: Core / Recall / Archival / Log / Neo4j Knowledge Graph
- Federated Collective Brain (GDPR-compliant, differential privacy)
- Credit-based pricing: $99 Studio / $299 Agency / Enterprise

---

## Pricing

| Tier | Price | Credits | Target |
|---|---|---|---|
| Studio | $99/mo | 500 | Solo devs |
| Agency | $299/mo | 2,000 + white-label | Dev shops |
| Enterprise | Custom | Unlimited + SLAs | Corps |

1 credit = $0.05 compute.

---

## Skills Library

11 battle-tested playbooks agents use instead of figuring things out from scratch:

```
skills/auth/       → supabase-auth, clerk-auth
skills/payments/   → stripe-subscriptions, stripe-one-time
skills/ui/         → dashboard-layout, landing-page, data-table-crud
skills/api/        → rest-crud, webhook-handler
skills/deploy/     → vercel-nextjs
skills/testing/    → playwright-e2e
```

---

## License

Private — Preetham © 2026
