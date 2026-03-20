# PROJECT_INDEX.md — Forge v2.0
> Load this FIRST every session. Navigation hub + current status.

---

## PROJECT STATUS
- **Phase:** Month 1–2 (Core Loop)
- **Started:** March 2026
- **Current Sprint:** Stage 4 frontend baseline (14-screen React conversion)
- **Blockers:** Stitch asset extraction (environment/auth restrictions)

---

## RESEARCH COMPLETED ✅
- [x] Strategic Analysis (Research Report 1)
- [x] Architecture Deep-Dive (Research Report 2)
- [x] Feasibility Study (Research Report 3)
- [x] Competitor analysis: Devin, Cursor, Lovable, Bolt, Replit, v0, OpenHands, Oz (Warp), Manus, Google ADK
- [x] Microsoft AI Agents for Beginners (15 lessons mapped)
- [x] Google ADK docs (A2A, Parallel/Loop agents, Resume/HITL)
- [x] Warp Oz docs (Skills system, cloud agents, steer mode)
- [x] Manus docs (all 10 features mapped and copied into Forge)
- [x] Founding architecture document created (forge-founding-document.html)
- [x] Memory bank system created (all 10 .md files)
- [x] Features roadmap created (FEATURES.md + 3 seed skill files)

---

## ARCHITECTURE DECISIONS MADE ✅
- [x] Credit-based pricing (not flat-rate) — DECISION-001
- [x] Technical agencies as target (not non-developers) — DECISION-002
- [x] Next.js + Supabase first (scope lock) — DECISION-003
- [x] HITL gate mandatory — DECISION-004
- [x] E2B sandbox per agent — DECISION-005
- [x] LangGraph for orchestration — DECISION-006
- [x] Neo4j for Temporal Knowledge Graph — DECISION-007
- [x] PydanticAI for output validation — DECISION-008
- [x] Maintenance Agent monitor-only — DECISION-009
- [x] Federated Learning for Collective Brain — DECISION-010
- [x] Hybrid LangGraph + Google ADK — DECISION-011
- [x] 2-pass screenshot→code pipeline — DECISION-012
- [x] Progressive Disclosure Skills system — DECISION-013
- [x] Per-agent owned sandboxes (OpenHands model) — DECISION-014

---

## WHAT IS DONE ✅
- [x] Full architecture designed
- [x] Founding document written
- [x] Pricing model finalized
- [x] 15-agent roster finalized
- [x] Tech stack finalized
- [x] 12-month roadmap written
- [x] Memory bank files created
- [x] Features roadmap (Manus-inspired) created
- [x] 3 seed Skill files created

---

## IN PROGRESS 🔄
- [x] ForgeState Pydantic model (`forge/core/state.py`)
- [x] LangGraph StateGraph scaffold (`forge/core/graph.py`)
- [x] PM Agent baseline implementation (`forge/agents/pm_agent.py`)
- [x] Architect baseline implementation (`forge/agents/architect.py`)
- [x] BaseAgent runtime scaffold (`forge/agents/base.py`)
- [x] E2B runtime scaffold (`forge/sandbox/e2b_runtime.py`)
- [x] Git artifact transport scaffold (`forge/sandbox/git_transport.py`)
- [x] Frontend route conversion for 14 Forge product screens (`platform/app/**/*`)
- [x] Shared UI shell + screen primitives (`platform/components/layout/*`)
- [x] Platform config restoration (`platform/tsconfig.json`, `next.config.ts`, `tailwind.config.ts`, `postcss.config.js`)
- [ ] Stage 3 tests (`tests/integration/test_stage3.py`)

---

## NEXT UP 📋
- [ ] Stitch asset/code import for all 14 screens (via accessible exports)
- [ ] Visual fidelity pass against source mocks per screen
- [ ] Playwright coverage for primary dashboard/project flows
- [ ] Security Agent (Semgrep + Snyk scaffold)
- [ ] Testing Agent loop scaffold
- [ ] Critic quality gate hardening
- [ ] HITL approval gate UI (Next.js dashboard)
- [ ] FinOps Agent (token budget enforcement)
- [ ] Vercel deploy pipeline
- [ ] 10 Skill files (Phase 1 library)
- [ ] Credit system (Stripe)
- [ ] Client dashboard

---

## FILE MAP
| File | Purpose | Update when |
|---|---|---|
| SYSTEM_PROMPT.md | Paste into every AI session | Project direction changes |
| PROJECT_INDEX.md | This file — status + navigation | After every milestone |
| NOW.md | Active task working memory | Start + end of every session |
| ARCHITECTURE.md | Full system architecture | Structural changes |
| AGENTS.md | All 15 agents — roles, LLMs, sandboxes | Agent behavior changes |
| TECH_STACK.md | Every tech choice + rationale | Tech choices change |
| ROADMAP.md | 12-month milestones | Milestones complete |
| DECISIONS.md | Architectural decisions log | Any major decision made |
| CONSTRAINTS.md | Hard rules — never violate | Constraints evolve |
| API_CONTRACTS.md | Agent-to-agent Pydantic schemas | Schemas change |
| FEATURES.md | Full feature roadmap (Manus-inspired) | Features added/shipped |
| skills/*.skill.md | Reusable agent playbooks | Skills validated/improved |

---

## COMPETITIVE LANDSCAPE (decided)
| Competitor | Gap | Forge answer |
|---|---|---|
| Lovable/Bolt | Brittle at scale, no maintenance | Full SDLC + maintenance agent |
| Devin | $500/mo, needs senior devs | $299/mo, HITL not babysitting |
| Cursor | IDE only, no end-to-end | Full build → deploy pipeline |
| OpenHands | General, no memory, no specialization | 15 specialists + Knowledge Graph |
| Manus | General agent, no HITL, no moat | Specialized + Collective Brain |
| Oz (Warp) | Internal dev tool, not client-facing | Agency platform for client work |

*v2.0 — March 2026*
