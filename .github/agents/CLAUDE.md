# CLAUDE.md — Forge Project
# Claude Code reads this file automatically from your project root.
# This gives Claude Code full context about Forge without pasting anything.

## WHO I AM
Preetham — developer in Bengaluru building Forge as a startup.

## WHAT FORGE IS
Forge is a 15-agent AI platform that acts as a software development agency.
Users describe a web app → agents build, deploy, and monitor it.
Every production deploy requires human approval (HITL gate — non-negotiable).

## MEMORY BANK LOCATION
All project context lives in:
```
forge-memory/       ← 10 .md files — architecture, agents, decisions, constraints
forge-features/     ← FEATURES.md + 11 SKILL.md files
FORGE_CODING_PROMPT.md  ← Full coding prompt with stage tracker
```

## READ BEFORE EVERY SESSION
1. forge-memory/PROJECT_INDEX.md — what's done / in progress / next
2. forge-memory/NOW.md — active sprint task
3. forge-memory/CONSTRAINTS.md — 14 hard rules (never violate)

## HARD CONSTRAINTS
- C1: HITL gate mandatory — DevOps Agent blocked without human approval token
- C2: Per-agent E2B sandbox — each agent has its own isolated environment
- C3: Credit-based pricing only — no flat-rate tiers
- C4: Phase 1 = Next.js + Supabase only
- C5: PydanticAI validates every single agent output
- C6: FinOps Agent kills runaway loops (token budget enforced)
- C7: Maintenance Agent never auto-applies — proposes PRs only
- C8: No raw code in Collective Brain — Federated Learning only

## CURRENT PHASE
Month 1–2: Core Loop.
Building: ForgeState → LangGraph graph → PM Agent → Architect → Build Agents.
Full pipeline sequence in: FORGE_CODING_PROMPT.md → "Build Stages" section.

## TECH STACK SUMMARY
- Orchestration: LangGraph + Google ADK (hybrid)
- Agents: Claude Opus/Sonnet/Haiku + Gemini 3 Pro + Perplexity Sonar
- Execution: E2B per-agent sandboxes (OpenHands-style runtime loop)
- Memory: Neo4j (Knowledge Graph) + Pinecone + ChromaDB + Redis + Mem0
- RAG: LlamaIndex managing 3 pipelines
- Platform: Next.js 15 + FastAPI + PostgreSQL + Clerk + Stripe
- Full details: forge-memory/TECH_STACK.md

## CODE STYLE
- Python: async/await, Pydantic v2, type hints on all functions
- TypeScript: strict mode, Zod validation, server components default
- All code: production quality with inline comments
- Commits: "feat(scope): description" format

## AFTER COMPLETING ANY TASK
Always update forge-memory/NOW.md with summary of what was done and next step.
