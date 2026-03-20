# ARCHITECTURE.md — Forge System Architecture v2.0
> Canonical architecture. Add to DECISIONS.md before changing anything here.

---

## SYSTEM OVERVIEW

```
User Input (text / screenshot / voice / email)
         │
         ▼
┌─────────────────────────────────────────────────────────┐
│                    FORGE PLATFORM                        │
│                                                          │
│  PM Agent → Architect → Design                          │
│                       → [Frontend ∥ Backend] (ADK Parallel)
│                       → Security → Testing (ADK Loop)   │
│                       → Critic                          │
│                       → [HITL GATE — ADK Resume]        │
│                       → DevOps → Deploy                 │
│                                                          │
│  Always running: FinOps Agent (budget enforcement)      │
│  Always running: Research Agent (on-demand lookup)      │
│  Post-deploy: Maintenance Agent (monitor → PR proposal) │
│  Post-deploy: Docs Agent (auto-generate on every commit)│
└─────────────────────────────────────────────────────────┘
         │
         ▼
Deployed App (Vercel + Railway + Cloudflare)
```

---

## ORCHESTRATION LAYER

### Hybrid: LangGraph + Google ADK

**LangGraph** owns:
- Master ForgeState Pydantic object (single source of truth)
- Overall pipeline routing + conditional edges
- Checkpointing (every 2 min, PostgreSQL persistence)
- LangSmith observability + distributed tracing
- Failure recovery + task resumption

**Google ADK** handles:
- `ParallelAgent` — Frontend ∥ Backend ∥ Design running simultaneously
- `LoopAgent` — Testing Agent retry loop (max 5 iterations until tests pass)
- `SequentialAgent` — PM → Architect sequence
- `Resume` — HITL gate pause + wait for human + resume with state preserved
- `A2A Protocol` — dynamic agent discovery and spawning via AgentCard registry

```python
# Example: parallel build inside LangGraph node
from google.adk.agents import ParallelAgent
from langgraph.graph import StateGraph

forge_graph = StateGraph(ForgeState)

async def build_node(state: ForgeState):
    parallel = ParallelAgent(
        sub_agents=[frontend_agent, backend_agent, design_agent]
    )
    return await parallel.run(state.tech_spec)

async def test_node(state: ForgeState):
    loop = LoopAgent(
        sub_agents=[testing_agent],
        max_iterations=5
    )
    return await loop.run(state)

forge_graph.add_node("build", build_node)
forge_graph.add_node("test", test_node)
```

### Execution Patterns
| Pattern | Used by | Description |
|---|---|---|
| LATS | Architect, ML Agent | Tree search for complex decisions |
| Evaluator-Optimizer | Testing Agent (LoopAgent) | Write failing tests → force fix → retest |
| Reflection | Critic Agent | Isolated context window review |
| ReAct | Backend, DevOps, Research | Tool use + reasoning interleaved |
| OpenHands Loop | All build agents | observe → think → act → repeat |

---

## AGENT RUNTIME MODEL (OpenHands-style)

Each build agent runs an **observe → think → act** loop inside its own E2B sandbox.
This is NOT one-shot code generation. Agents develop software like a human.

```python
class AgentRuntime:
    sandbox: E2BSandbox      # isolated compute (purpose-specific image)
    filesystem: GitBackedFS  # git-backed file system (artifact transport)
    browser: PlaywrightBrowser  # visual verification

    async def run(self, task: AgentTask) -> AgentOutput:
        for iteration in range(self.max_iterations):  # max 20
            observation = await self.observe()   # see current state
            action = await self.think(observation)  # LLM decides
            result = await self.act(action)       # execute in sandbox
            self.finops.record(tokens_used)        # budget check

            if self.task_complete(result):
                await self.commit_artifacts()  # git commit
                break
            if self.finops.budget_exceeded():
                raise BudgetExceededError()

    async def observe(self) -> Observation:
        return Observation(
            filesystem=await self.sandbox.list_files(),
            last_command_output=self.last_result,
            build_errors=await self.sandbox.get_errors(),
            screenshot=await self.browser.screenshot(),  # visual state
        )

    async def act(self, action: Action) -> Result:
        match action.type:
            case "bash":   return await self.sandbox.run(action.cmd)
            case "write":  return await self.filesystem.write(action.path, action.content)
            case "read":   return await self.filesystem.read(action.path)
            case "browse": return await self.browser.screenshot(action.url)
            case "search": return await research_agent.query(action.query)
```

### Per-Agent Sandbox Images
| Agent | Docker Image | Key tools |
|---|---|---|
| Frontend | `node:20-alpine` | next, tailwind, playwright |
| Backend | `python:3.11-slim` | fastapi, supabase-py, pytest |
| Security | `semgrep/semgrep` | semgrep, snyk, bandit |
| Testing | `playwright:latest` | playwright, jest, pytest |
| DevOps | `alpine:latest` | vercel-cli, railway-cli, wrangler |
| ML | GPU image via Modal | pytorch, transformers, jupyter |
| PM / Architect / Critic | None — pure reasoning | No sandbox needed |

### Artifact Transport (Git-based)
```
Frontend Agent → git commit "feat: frontend components" → branch: forge/build
Backend Agent  → git commit "feat: api routes"         → branch: forge/build
Security Agent → git pull → scan → git commit "fix: security issues"
Testing Agent  → git pull → run tests → git commit "test: passing"
Critic Agent   → git pull → review → verdict
DevOps Agent   → git pull → deploy (ONLY with HITL approval token)
```

---

## MEMORY ARCHITECTURE (5 Tiers)

### Tier 1 — Core Memory (always in context)
- Client brand, current sprint goal, approved stack, conventions
- **Storage:** Hardcoded in system prompt per session
- **Size:** Token-limited, kept minimal

### Tier 2 — Recall Memory (recent sessions)
- Last 30 days of agent actions + decisions
- **Storage:** Redis (TTL 30 days) via Mem0
- **Compression:** Nightly ACC (Agent Cognitive Compressor)

### Tier 3 — Archival Memory (full history)
- Complete codebase RAG, full project history, error+fix library
- **Storage:** ChromaDB (per-project) + Pinecone (Collective Brain)
- **Access:** search_archival() tool call — never auto-loaded

### Tier 4 — Log Memory (physical state)
- Per-project `/memory/` folder, Git-versioned
- `INDEX.md` — loaded every session
- `NOW.md` — current task
- `logs/YYYY-MM-DD.md` — episodic logs
- **Compression:** Nightly ACC cron

### Tier 5 — Temporal Knowledge Graph (relationships)
- **Storage:** Neo4j / Graphiti
- Client preferences, stack decisions, incident history, brand constraints
- Queried by EVERY agent before any action
- **This is the core of Brand Memory's defensibility**
- **Episodic:** PostgreSQL hypertables (timestamped events)
- **Semantic:** Pinecone + pgvector (codebase + docs)
- **Procedural:** Neo4j (relationships + preferences)

---

## SKILLS SYSTEM (Progressive Disclosure)

Copied from Manus + upgraded with Collective Brain self-improvement.

```
Level 1 — Metadata (~100 tokens per skill, always loaded)
  name, description, tags, category
  → Agent knows ALL skills exist at startup

Level 2 — Instructions (<5k tokens, loaded when skill is triggered)
  Full SKILL.md content
  Triggered by: Architect maps task → skill, or user types /skills

Level 3 — Resources (on demand, referenced from Level 2)
  Templates, schemas, example files
  Loaded only when Level 2 instructions reference them
```

```python
class ForgeSkill:
    metadata: SkillMetadata      # L1 — always in context
    instructions: str            # L2 — loaded on trigger
    resources: list[SkillResource]  # L3 — loaded on demand

    @classmethod
    def load_all_metadata(cls) -> list[SkillMetadata]:
        # Returns ~100 tokens per skill — loads ALL at startup
        return [s.metadata for s in cls.all_skills()]
```

---

## RAG PIPELINES (3, via LlamaIndex)

### Pipeline 1 — Collective Brain RAG
- **Vector DB:** Pinecone
- **Embeddings:** OpenAI text-embedding-3-large
- **Content:** Anonymous project patterns, error+fix library
- **Privacy:** Federated Learning — encrypted param updates only
- **Update:** Self-improving — Collective Brain notes in every SKILL.md

### Pipeline 2 — Codebase RAG
- **Vector DB:** ChromaDB (per-project)
- **Chunking:** Code-aware (function/class level)
- **Content:** Full codebase, git history, comments

### Pipeline 3 — Domain Knowledge RAG
- **Source:** context7 MCP + LlamaIndex
- **Content:** Next.js docs, Supabase docs, OWASP rules, HIPAA/PCI standards

---

## SCREENSHOT → CODE PIPELINE (2-pass)

```
Pass 1 — Vision model ONLY (no code)
  Image → Gemini 3 Pro → SPEC_EXTRACTION_PROMPT → full spec document
  Extracts: exact hex colors, spacing values, font sizes, component list,
            layout pattern, border radius, typography, what's ambiguous

  [Optional HITL: show extracted spec to user for correction]

Pass 2 — Code model ONLY (no vision)
  Spec document → Claude Sonnet → Next.js components
  Uses EXACT values from spec — zero guessing

Pass 3 — Visual verify loop
  Render in sandbox → Playwright screenshot → compare with original
  Similarity ≥88%? → pass
  Similarity <88%? → Gemini diffs the two images → Claude fixes → repeat
```

---

## HITL GATE (ADK Resume pattern)

Non-negotiable. No production deploy without human approval.

```python
# Gate flow
1. Critic Agent approves output
2. System generates HITLPayload:
   - Git diff (all changed files)
   - Plain-English impact summary (max 200 words)
   - Risk level: low / medium / high
   - Rollback plan
   - Security scan result
   - Test coverage %
3. ADK Resume pauses the agent session
4. Human receives notification (dashboard + email)
5. Human actions:
   APPROVE → cryptographic token issued → DevOps deploys
   REJECT  → reason sent back → pipeline restarts from failed agent
   STEER   → human joins live session to redirect mid-build
   PAUSE   → session paused, resumes later
6. DevOps Agent BLOCKED until valid approval token present
```

---

## SECURITY ARCHITECTURE
- **Code execution:** E2B per-agent sandbox — generated code NEVER runs on host
- **Input sanitization:** Prompt injection detection on ALL user inputs
- **SAST:** Semgrep (OWASP Top 10 + custom Forge ruleset)
- **DAST:** Snyk (dependency scanning)
- **Multi-tenancy:** Strict isolation — no cross-tenant data access
- **API Gateway:** Kong (rate limiting, auth, logging)
- **Circuit Breaker:** LLM API fallbacks: Opus → Sonnet → Haiku
- **Collective Brain:** Federated Learning + Differential Privacy (GDPR Art. 5)

---

## INFRASTRUCTURE
| Layer | Technology |
|---|---|
| Platform frontend | Next.js 15 (App Router, TypeScript) |
| Platform backend | FastAPI (Python 3.11, async) |
| Database | PostgreSQL (via Supabase) |
| Cache | Redis |
| File storage | Cloudflare R2 |
| Deploy (user apps) | Vercel (frontend) + Railway (backend) |
| DNS/CDN/SSL | Cloudflare |
| GPU compute | Modal |
| Observability | LangSmith + OpenTelemetry + Sentry |
| Auth | Clerk |
| Payments | Stripe (subscriptions + credit purchases) |

*v2.0 — March 2026*
