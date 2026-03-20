# ROADMAP.md — 12-Month Build Plan v2.0
> Update status column as milestones are hit.

---

## MONTH 1–2: Core Loop ← WE ARE HERE

**Goal:** One complete end-to-end build on a simple Next.js + Supabase test app.

| Milestone | Status |
|---|---|
| All memory bank files created + updated | ✅ Done |
| FEATURES.md + seed Skills created | ✅ Done |
| ForgeState Pydantic model (`forge/core/state.py`) | 📋 Next |
| LangGraph StateGraph scaffold (`forge/core/graph.py`) | 📋 Next |
| Per-agent E2B runtime (`forge/sandbox/e2b_runtime.py`) | 📋 Next |
| PM Agent — text → PRDSchema | 📋 Next |
| Architect Agent — PRD → TechSpec + Skill mapping | ⬜ |
| Frontend Agent — Gemini + v0.dev + visual verify loop | ⬜ |
| Backend Agent — Claude Sonnet + Supabase | ⬜ |
| Git artifact transport between agents | ⬜ |
| HITL approval gate (ADK Resume) | ⬜ |
| HITL dashboard UI (Next.js — diff + plain English) | ⬜ |
| Vercel deploy pipeline | ⬜ |
| 10 Forge Skills (Phase 1 library) | 3/10 done |
| FinOps Agent (token budget enforcement) | ⬜ |
| 10 beta agency users (Bengaluru) | ⬜ |
| Token cost tracking per build | ⬜ |

### Phase 1 Skills to complete (7 remaining):
- [ ] `clerk-auth.skill.md`
- [ ] `stripe-one-time.skill.md`
- [ ] `landing-page.skill.md`
- [ ] `data-table-crud.skill.md`
- [ ] `rest-crud.skill.md`
- [ ] `webhook-handler.skill.md`
- [ ] `vercel-deploy.skill.md`

---

## MONTH 3–4: Moat Features

| Milestone | Status |
|---|---|
| Temporal Knowledge Graph (Neo4j + Graphiti) | ⬜ |
| Maintenance Agent (nightly scan → PR proposal only) | ⬜ |
| Scheduled Tasks (BullMQ cron for Maintenance Agent) | ⬜ |
| Collective Brain RAG v1 (seed data from beta builds) | ⬜ |
| Credit-based billing (Stripe subscriptions + credit top-ups) | ⬜ |
| Client portal (HITL dashboard + build progress) | ⬜ |
| Custom domain deploy | ⬜ |
| Forge Reports (auto-generate PDF after every build) | ⬜ |
| Cloud Browser upgrade (full visual Playwright session) | ⬜ |
| Forge Collab (owner/developer/client roles) | ⬜ |
| Wide Research Mode (parallel Research sub-agents) | ⬜ |

---

## MONTH 5–6: Quality & Trust

| Milestone | Status |
|---|---|
| Security Agent (Semgrep + Snyk + Bandit) | ⬜ |
| Testing Agent (ADK LoopAgent — Evaluator-Optimizer) | ⬜ |
| Critic Agent (isolated context window review) | ⬜ |
| Design Agent (2-pass screenshot→spec→code pipeline) | ⬜ |
| LangSmith full observability | ⬜ |
| SOC 2 Type II process started | ⬜ |
| Mail Forge (email trigger → build pipeline) | ⬜ |
| Browser Operator (Testing Agent operates browser like QA) | ⬜ |
| HITL Steer Mode (join live session to redirect agent) | ⬜ |
| First paying agency customers | ⬜ |

---

## MONTH 7–9: Expand & Enterprise

| Milestone | Status |
|---|---|
| Second stack (T3 Stack or React + Firebase) | ⬜ |
| ML Agent (Modal GPU compute) | ⬜ |
| Federated Collective Brain (differential privacy) | ⬜ |
| SOC 2 Type II certification | ⬜ |
| Data Analysis feature (Growth Agent + data uploads → components) | ⬜ |
| Multimedia Processing (voice→PRD via Whisper, video→rebuild) | ⬜ |
| Google ADK A2A protocol for dynamic spawning | ⬜ |
| First enterprise pilot (Bengaluru GCC or Fortune 500 R&D) | ⬜ |

---

## MONTH 10–12: Scale & Launch

| Milestone | Status |
|---|---|
| Growth Agent (GA4 + Posthog integration) | ⬜ |
| Skills self-improvement (Collective Brain updates skills) | ⬜ |
| Skills marketplace (agencies publish/import skills) | ⬜ |
| White-label platform | ⬜ |
| Public API | ⬜ |
| Bengaluru → global agency market expansion | ⬜ |
| Target: $500K ARR | ⬜ |

---

## 5-YEAR TARGETS
- $50–200M ARR
- 1–2% capture of $10B SAM
- 1,000+ agencies on platform
- Collective Brain: 100,000+ project patterns
- Skills library: 500+ verified skills

---

## COMPETITORS TO BEAT
| Competitor | Their gap | Our answer |
|---|---|---|
| Lovable ($6.6B) | Brittle at scale, no maintenance | Full SDLC + Knowledge Graph |
| Devin ($10.2B / $73M ARR) | $500/mo, enterprise only | $299/mo, HITL not babysitting |
| Manus | General agent, no moat, no HITL | Specialized + Collective Brain |
| Oz (Warp) | Internal dev tool, not agency | Client-facing agency platform |
| Bolt.new | Prototype only, tech debt | Production-grade + maintained |

*v2.0 — March 2026*
