# AGENTS.md — All 15 Agents v2.0
> Complete agent reference. Update when agent behavior or runtime changes.

---

## EXECUTION ORDER

```
PM Agent (text → PRD)
  └→ Architect Agent (PRD → TechSpec + Skill mapping)
       ├→ Design Agent     [OWN SANDBOX: figma-api + browser]
       ├→ Frontend Agent   [OWN SANDBOX: node:20 + next + tailwind]  ← parallel
       └→ Backend Agent    [OWN SANDBOX: python:3.11 + supabase-cli] ← parallel
            └→ Security Agent  [OWN SANDBOX: semgrep + snyk]
                 └→ Testing Agent   [OWN SANDBOX: playwright + jest + pytest]
                      └→ Critic Agent    [NO SANDBOX — pure reasoning]
                           └→ ══ HITL GATE (human approval) ══
                                └→ DevOps Agent  [OWN SANDBOX: vercel-cli + railway]
                                     └→ Deployed App ✓

Always: FinOps Agent (monitors token spend for all above)
Always: Research Agent (on-demand lookup for any agent)
Post:   Maintenance Agent (nightly scans → PR proposals)
Post:   Docs Agent (auto-generate on every commit)
```

---

## AGENT RUNTIME PATTERN
Every build agent runs: **observe → think → act → repeat** (max 20 iterations)
Pure reasoning agents (PM, Architect, Critic) run single-shot with reflection.
All output is **PydanticAI-validated** before passing downstream.

---

## COMMAND LAYER

### 1. Orchestrator
| Field | Value |
|---|---|
| LLM | Claude Opus 4.5 |
| Role | CEO — coordinates all agents |
| Sandbox | None — pure reasoning + tool calls |
| Pattern | ReAct (tool use + reasoning) |
| Tools | spawn_agent(), escalate_to_hitl(), read_state(), write_state(), a2a_discover() |
| Budget | Highest — controls all sub-budgets |

**Core behavior:** Receives user request → writes spawn plan → calls PM Agent → monitors FinOps → escalates to HITL when risk is high. Never writes code.

---

### 2. PM Agent *(New — Research Mandated)*
| Field | Value |
|---|---|
| LLM | Claude Sonnet 4.5 |
| Role | Product Manager — vague input → structured PRD |
| Sandbox | None — pure reasoning |
| Pattern | Single-shot with reflection |
| Input | Raw text, email, voice transcript, screenshot |
| Output | PRDSchema (Pydantic validated) |
| Tools | search_archival(), read_brand_memory(), transcribe_audio() |
| Multimedia | Accepts voice notes (Whisper transcription), documents, images |

**Core behavior:** Turns ANY client input format into a structured PRD. Prevents specification drift — the #1 cause of multi-agent failure.

---

### 3. Architect Agent
| Field | Value |
|---|---|
| LLM | Claude Opus 4.5 |
| Role | System designer — PRD → TechSpec + Skill mapping |
| Sandbox | None — pure reasoning |
| Pattern | LATS (tree search for complex designs) |
| Input | PRDSchema + Knowledge Graph query |
| Output | TechSpecSchema + skill_assignments dict |
| Tools | query_knowledge_graph(), search_archival(), read_docs() |
| MCP | context7 (official Next.js + Supabase docs) |

**Core behavior:** Queries client's Temporal Knowledge Graph for preferences/constraints BEFORE designing. Maps each task to the best matching Skill from the library. Never writes production code.

---

## BUILD LAYER

### 4. Frontend Agent
| Field | Value |
|---|---|
| LLM | Gemini 3 Pro (primary) + v0.dev API (component generation) |
| Role | UI/UX — builds all frontend code |
| Sandbox | `node:20-alpine` + Next.js + Tailwind + Playwright |
| Pattern | OpenHands loop (max 20 iterations) |
| Input | TechSpecSchema + wireframes from Design Agent + active Skill |
| Output | React components, pages, styles (Next.js App Router) |
| Tools | write_file(), run_bash(), browser_screenshot(), read_file() |
| MCP | figma, playwright, context7 |
| Runs parallel to | Backend Agent, Design Agent |
| Visual verify | Screenshots rendered app, compares with design spec ≥88% |

---

### 5. Backend Agent
| Field | Value |
|---|---|
| LLM | Claude Sonnet 4.5 |
| Role | API, auth, business logic |
| Sandbox | `python:3.11-slim` + supabase-cli + fastapi + pytest |
| Pattern | OpenHands loop (max 20 iterations) |
| Input | TechSpecSchema (API routes, data models) |
| Output | API routes, Supabase schema SQL, auth config |
| Tools | write_file(), run_bash(), execute_sql_in_sandbox() |
| MCP | supabase, postgres, stripe |
| Runs parallel to | Frontend Agent |

---

### 6. Design Agent *(New — Research Mandated)*
| Field | Value |
|---|---|
| LLM | Gemini 3 Pro (multimodal) |
| Role | Wireframes + design spec BEFORE any code is written |
| Sandbox | Browser-based (figma API + cloud browser) |
| Pattern | 2-pass screenshot pipeline (if screenshot provided) |
| Input | PRDSchema + optional: screenshot / Figma URL |
| Output | WireframeSchema + design tokens (exact hex/px values) |
| MCP | figma |
| Runs before | Frontend Agent (feeds it exact design tokens) |

**Screenshot mode:** Pass 1 = Gemini extracts full spec (colors, spacing, fonts, components). Pass 2 = Frontend Agent builds from spec. Visual verify loop ≥88%.

---

### 7. ML Agent
| Field | Value |
|---|---|
| LLM | Claude Opus 4.5 (extended thinking mode) |
| Role | AI/ML features, model training |
| Sandbox | GPU image via Modal (PyTorch + Transformers + CUDA) |
| Pattern | LATS |
| Input | ML requirements from TechSpec |
| Output | Model code, training scripts, inference endpoints |
| MCP | huggingface, jupyter |
| Spawned | Only when project has explicit ML requirements |

---

### 8. DevOps Agent
| Field | Value |
|---|---|
| LLM | Claude Sonnet 4.5 |
| Role | Infrastructure + deployment (ONLY post-HITL) |
| Sandbox | `alpine:latest` + vercel-cli + railway-cli + wrangler |
| Pattern | ReAct |
| Input | Approved code + TechSpec + **valid HITL approval token** |
| Output | Live deploy URL |
| MCP | cloudflare, vercel, railway |
| **HARD RULE** | Will NOT execute without valid HITL approval token |

---

### 9. FinOps Agent *(New — Research Mandated)*
| Field | Value |
|---|---|
| LLM | Claude Haiku 4.5 |
| Role | Real-time cost tracking + budget enforcement |
| Sandbox | None — event-driven sidecar |
| Pattern | Event-driven (runs alongside all agents, not in main pipeline) |
| Input | Token usage events from all agents |
| Output | Cost reports, budget alerts, kill signals |
| Tools | read_token_usage(), emit_kill_signal(), write_cost_report() |
| Action | Kills runaway agents when budget threshold breached |

**Default budgets (tokens):**
```python
DEFAULT_BUDGETS = {
    "pm_agent": 10_000,
    "architect": 50_000,
    "frontend": 100_000,
    "backend": 100_000,
    "design": 30_000,
    "security": 30_000,
    "testing": 50_000,
    "critic": 20_000,
    "devops": 15_000,
}
```

---

## QUALITY LAYER

### 10. Security Agent
| Field | Value |
|---|---|
| LLM | Claude Opus 4.5 |
| Role | SAST/DAST — block vulnerable code from shipping |
| Sandbox | `semgrep/semgrep` + snyk + bandit |
| Pattern | Reflection |
| Input | All generated code (pulls from git) |
| Output | SecurityReport (PASS / FAIL + findings) |
| Tools | run_semgrep(), run_snyk(), check_owasp_top10() |
| On FAIL | Blocks pipeline → sends findings back to originating agent |

---

### 11. Testing Agent
| Field | Value |
|---|---|
| LLM | Claude Sonnet 4.5 |
| Role | Write and run tests until all pass |
| Sandbox | `playwright:latest` + jest + pytest |
| Pattern | ADK LoopAgent — Evaluator-Optimizer (writes failing tests first) |
| Input | Generated code + TechSpec acceptance criteria |
| Output | TestResults (PASS / FAIL + coverage) |
| Tools | run_in_e2b(), playwright_test(), pytest(), jest() |
| MCP | playwright |
| Loop exits when | All tests pass or max 5 iterations reached |

---

### 12. Critic Agent
| Field | Value |
|---|---|
| LLM | Claude Opus 4.5 |
| Role | Final quality gate before HITL |
| Sandbox | None — **isolated context window** (does NOT share context with other agents) |
| Pattern | Reflection |
| Input | All code + security report + test results |
| Output | CriticVerdict: APPROVE / REJECT + summary + risk level |
| Tools | None — pure reasoning only |

---

## INTELLIGENCE & PERSISTENCE LAYER

### 13. Research Agent
| Field | Value |
|---|---|
| LLM | Perplexity Sonar |
| Role | Real-time information retrieval |
| Sandbox | None |
| Pattern | Single-shot, citation-first |
| Input | Search query from any agent |
| Wide Mode | Spawns 5-10 parallel sub-agents for deep research |
| MCP | brave-search, context7 |

---

### 14. Maintenance Agent
| Field | Value |
|---|---|
| LLM | Claude Sonnet 4.5 |
| Role | Post-deploy monitoring + scoped PR proposals |
| Sandbox | None — reads external APIs |
| Pattern | Scheduled (nightly cron via BullMQ) |
| Input | Sentry errors, Uptime Robot alerts, Lighthouse scores |
| Output | PR draft proposals (NEVER auto-applied) |
| MCP | sentry |
| Schedule | Nightly 2 AM: scan → report → propose PRs |
| **HARD RULE** | MONITORS ONLY. Never autonomously applies any code change. |

---

### 15. Docs Agent
| Field | Value |
|---|---|
| LLM | Claude Haiku 4.5 |
| Role | Auto-generate docs on every code change |
| Sandbox | None |
| Pattern | Event-triggered (on every git commit) |
| Input | Code diffs, function signatures, API routes |
| Output | API docs, changelogs, architecture notes, client report PDF |

---

## AGENT VALIDATION CHAIN
```
Agent output → PydanticAI schema validation
   ├── PASS → pass to next agent
   └── FAIL → retry (max 3)
                ├── PASS on retry → continue
                └── FAIL after 3 → Critic Agent
                                     ├── PASS → continue with warning
                                     └── FAIL → escalate to human
```

*v2.0 — March 2026*
