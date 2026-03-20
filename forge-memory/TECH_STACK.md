# TECH_STACK.md — Complete Technology Stack v2.0

---

## LLM ROUTER (via LiteLLM / Portkey)

| Task | Model | Cost | Why |
|---|---|---|---|
| Complex reasoning, architecture, security | Claude Opus 4.5 | $5/$25 per M | Best SWE-bench (80.9%), extended thinking |
| Code execution, standard build tasks | Claude Sonnet 4.5 | $3/$15 per M | 82% SWE, fast, cost-effective |
| UI generation, visual tasks, screenshot analysis | Gemini 3 Pro + v0.dev | Variable | #1 WebDev Arena, 1M context, multimodal |
| Routing, docs, summarization, FinOps | Claude Haiku 4.5 | $0.04/1M input | Lowest cost + latency |
| Real-time research, citations | Perplexity Sonar | Per-query | Citation-first, no hallucination |
| Large codebase context (>200k tokens) | Gemini 3 Pro | Variable | 1M token context window |
| ML Agent (thinking-heavy) | Claude Opus 4.5 (extended thinking) | $5/$25 per M | Best for complex reasoning chains |
| Audio transcription (voice → PRD) | OpenAI Whisper | Per minute | PM Agent multimedia input |

**Fallback chain:** Opus → Sonnet → Haiku (automatic on API failure)
**Gateway:** LiteLLM (primary) or Portkey (backup) for dynamic routing + cost tracking

---

## ORCHESTRATION

| Technology | Purpose |
|---|---|
| **LangGraph** | Master ForgeState graph, checkpointing, conditional routing |
| **Google ADK** | ParallelAgent (frontend∥backend), LoopAgent (testing), Resume (HITL), A2A protocol |
| **LangChain** | LLM + tool connections, prompt templates |
| **LangSmith** | Full observability, trace logging, evals, LLM monitoring |
| **DSPy** | Automatic prompt optimization for agent system prompts |
| **PydanticAI** | Schema validation on every agent output (non-negotiable) |

---

## MEMORY & RAG

| Technology | Purpose | Scope |
|---|---|---|
| **LlamaIndex** | Manages all 3 RAG pipelines | Platform-wide |
| **Pinecone** | Collective Brain vectors (anonymous patterns) | All tenants |
| **ChromaDB** | Per-project codebase RAG | Per project |
| **OpenAI text-embedding-3-large** | Embeddings for both vector DBs | Both |
| **Neo4j** | Temporal Knowledge Graph (relationships, preferences) | Per client |
| **Graphiti** | Agent-native Neo4j interface | Per client |
| **Mem0** | Long-term session memory management | Per user |
| **Redis** | Recall Memory, session state, BullMQ backing | Platform-wide |
| **PostgreSQL** (pgvector) | Episodic memory, structured data, hypertables | Platform-wide |

---

## AGENT SANDBOX & EXECUTION

| Technology | Purpose |
|---|---|
| **E2B** | Per-agent sandbox (each agent owns its own) |
| **Playwright** | Visual browser — screenshots, E2E, browser operator |
| **Git** (per-project repo) | Artifact transport between agent sandboxes |
| **Snyk** | Dependency vulnerability scanning (DAST) |
| **Semgrep** | Static analysis (SAST) — OWASP Top 10 ruleset |
| **Bandit** | Python security linting |
| **Modal** | GPU compute for ML Agent |

---

## PLATFORM INFRASTRUCTURE

| Layer | Technology | Notes |
|---|---|---|
| Platform frontend | Next.js 15 (App Router) | TypeScript + Tailwind |
| Platform backend | FastAPI (Python 3.11) | Async, type-safe |
| Primary database | PostgreSQL | Via Supabase |
| Cache | Redis | Sessions + BullMQ |
| Auth | Clerk | OAuth, JWT, sessions |
| Payments | Stripe | Subscriptions + credit top-ups |
| File storage | Cloudflare R2 | S3-compatible |
| Error monitoring | Sentry | Platform + deployed apps |
| Uptime monitoring | Uptime Robot | Client deployed apps |

---

## DEPLOYMENT & DEVOPS

| Layer | Technology | Used for |
|---|---|---|
| User app frontend | Vercel | Client Next.js app deploys |
| User app backend | Railway | Client API/backend deploys |
| DNS + CDN + SSL | Cloudflare | All domains |
| Message queue | BullMQ | Agent task queue + scheduled tasks |
| API Gateway | Kong | Rate limiting, auth, logging |
| Distributed tracing | OpenTelemetry | Cross-agent observability |
| Metrics | Prometheus + Grafana | Performance dashboards |
| CI/CD | GitHub Actions | Platform + skill testing |
| ML experiment tracking | MLflow | ML Agent model versioning |

---

## SECURITY STACK

| Tool | Role |
|---|---|
| Semgrep | SAST — static code analysis (OWASP Top 10) |
| Snyk | DAST — dependency + container vulnerability scan |
| Bandit | Python-specific security linting |
| Kong | API gateway — rate limiting + auth enforcement |
| E2B | Sandbox isolation — generated code never runs on host |
| Differential Privacy | Collective Brain — Federated Learning privacy budget |
| Clerk | Auth + session management |

---

## MCP SERVERS (20+)

**Universal (all agents)**
- `filesystem` — read/write project files
- `github` — repo, PRs, commits
- `memory` — agent memory operations
- `docker` — container management

**Frontend Agent**
- `figma` — design context + variables
- `playwright` — browser automation + testing
- `context7` — Next.js + Tailwind official docs

**Backend Agent**
- `supabase` — database + auth + storage
- `postgres` — direct DB queries
- `stripe` — payment operations

**DevOps Agent**
- `cloudflare` — DNS, SSL, Workers, R2
- `vercel` — deployment
- `railway` — backend deployment

**Research Agent**
- `brave-search` — web search
- `context7` — official framework docs

**Maintenance Agent**
- `sentry` — error monitoring
- `notion` — documentation updates
- `slack` / `discord` — team notifications

---

## MANUS-INSPIRED FEATURES STACK

| Feature | Technology |
|---|---|
| Skills system | SKILL.md files + LlamaIndex (progressive disclosure) |
| Scheduled Tasks | BullMQ cron + specific agent triggers |
| Mail Forge | Unique SMTP address per workspace → PM Agent pipeline trigger |
| Cloud Browser | Playwright persistent session (upgrade from headless-only) |
| Browser Operator | Playwright + computer-use pattern |
| Wide Research | Parallel Research sub-agents via ADK ParallelAgent |
| Forge Reports | Docs Agent → PDF/Markdown/Notion output |
| Voice → PRD | OpenAI Whisper → PM Agent |
| Data Analysis | Growth Agent + pandas + Recharts component generation |

---

## PYTHON DEPENDENCIES
```toml
[tool.poetry.dependencies]
python = "^3.11"
langgraph = "latest"
langchain = "latest"
langsmith = "latest"
pydantic = "^2.0"
pydantic-ai = "latest"
google-adk = "latest"        # ADK Parallel/Loop/A2A/Resume
llama-index = "latest"
chromadb = "latest"
pinecone-client = "latest"
neo4j = "latest"
graphiti-core = "latest"
mem0ai = "latest"
redis = "latest"
e2b = "latest"
litellm = "latest"
fastapi = "latest"
uvicorn = "latest"
stripe = "latest"
sentry-sdk = "latest"
opentelemetry-api = "latest"
bullmq = "latest"
dspy-ai = "latest"
openai = "latest"            # Whisper + embeddings
```

## JS/TS DEPENDENCIES
```json
{
  "dependencies": {
    "next": "15.x",
    "@clerk/nextjs": "latest",
    "stripe": "latest",
    "@stripe/stripe-js": "latest",
    "@supabase/supabase-js": "latest",
    "@supabase/ssr": "latest",
    "tailwindcss": "^3",
    "zod": "latest",
    "@sentry/nextjs": "latest"
  }
}
```

---

## ENVIRONMENT VARIABLES (structure only — no secrets)
```bash
# LLM APIs
ANTHROPIC_API_KEY=
GOOGLE_GENERATIVE_AI_API_KEY=
PERPLEXITY_API_KEY=
OPENAI_API_KEY=           # Whisper + embeddings only

# Platform
STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=
CLERK_SECRET_KEY=
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=

# Database
SUPABASE_URL=
SUPABASE_SERVICE_ROLE_KEY=
NEXT_PUBLIC_SUPABASE_URL=
NEXT_PUBLIC_SUPABASE_ANON_KEY=
DATABASE_URL=             # direct postgres

# Memory & RAG
PINECONE_API_KEY=
PINECONE_ENVIRONMENT=
NEO4J_URI=
NEO4J_USERNAME=
NEO4J_PASSWORD=
REDIS_URL=

# Execution
E2B_API_KEY=
MODAL_TOKEN_ID=
MODAL_TOKEN_SECRET=

# Observability
LANGSMITH_API_KEY=
SENTRY_DSN=

# Deploy
CLOUDFLARE_API_TOKEN=
VERCEL_TOKEN=
RAILWAY_TOKEN=
```

*v2.0 — March 2026*
