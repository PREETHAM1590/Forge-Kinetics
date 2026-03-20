# CONSTRAINTS.md — Hard Rules v2.0
> These CANNOT be changed without a DECISIONS.md entry.
> If any AI suggests violating these, push back immediately with the constraint ID.

---

## 🔴 ABSOLUTE CONSTRAINTS (never negotiate)

### C1 — HITL Gate is Mandatory
No production deployment without explicit human approval.
- DevOps Agent BLOCKED until valid HITL approval token (cryptographic)
- Token must include: approver ID, timestamp, signature
- Applies even for trivial changes, even in "auto mode"
- STEER mode exists — human can join live session, not just approve/reject
- **Reason:** Legal liability + EU AI Act 2026 + user trust

### C2 — Per-Agent Sandbox (no shared execution)
Each build agent runs in its OWN E2B sandbox with its own purpose-specific Docker image.
- Frontend Agent: node:20-alpine
- Backend Agent: python:3.11-slim
- Security Agent: semgrep/semgrep
- Testing Agent: playwright:latest
- DevOps Agent: alpine + CLIs
- Agents NEVER share a sandbox
- Generated code NEVER runs on host machine
- **Reason:** True isolation + parallel execution + audit trail per agent

### C3 — Credit-Based Pricing Only
No flat-rate unlimited tiers.
- Every resource-intensive operation costs credits
- User's credit balance checked BEFORE agent task starts
- FinOps Agent kills tasks exceeding per-task budget
- **Reason:** Multi-agent token consumption is multiplicative — flat-rate = bankruptcy

### C4 — PydanticAI Validation on Every Agent Output
Every agent output must be validated before downstream use.
- FAIL → retry max 3 → Critic escalation → human escalation
- No raw LLM text passed between agents
- **Reason:** 37% of multi-agent failures from inter-agent misalignment (MAST)

### C5 — Maintenance Agent Monitor-Only
Maintenance Agent NEVER autonomously applies code changes.
- Creates draft PRs only
- All its output flows through HITL gate
- No auto-merge, no scheduled auto-patch
- **Reason:** Production stability + EU AI Act + user control

### C6 — No Raw Code in Collective Brain
Federated Learning only.
- Encrypted parameter updates only cross tenant boundaries
- No user code, prompts, or project data shared between tenants
- Differential Privacy budget enforced
- GDPR Art. 5 data minimization
- **Reason:** Legal compliance + user trust

---

## 🟡 PHASE 1 CONSTRAINTS (expand with new DECISIONS.md entry)

### C7 — Next.js + Supabase Only
Phase 1 agents ONLY build Next.js + Supabase apps.
- All agent prompts, Skills, and RAG tuned for this stack
- Second stack: Month 7–9 (requires DECISIONS.md entry)
- **Reason:** Own one stack at 90%+ success rate > all stacks at 40%

### C8 — Vercel + Railway Deploy Targets Only
Phase 1 deploy targets: Vercel (frontend) + Railway (backend).
- No AWS, GCP, Azure, self-hosted in Phase 1
- Enterprise custom infra: Month 7+
- **Reason:** Minimize DevOps Agent complexity in MVP

---

## 🟢 SOFT CONSTRAINTS (guidelines, override with rationale)

### C9 — Max 3 PydanticAI Retries
Any agent that fails validation retries max 3 times before escalating.
- Prevents infinite retry loops
- After 3 failures → Critic → human

### C10 — 30-Minute Agent Timeout
Single agent task times out after 30 minutes.
- LangGraph checkpoint saved at timeout
- Task can be resumed manually
- FinOps logs timeout for cost analysis

### C11 — Max 20 Spawned Agents, Depth 3
Spawn Engine limits: 20 concurrent agents, hierarchy depth 3.
- Prevents runaway spawning
- Prevents context loss in deep hierarchies

### C12 — Checkpoint Every 2 Minutes
LangGraph saves state checkpoint every 2 minutes during execution.
- Enables failure recovery
- Enables task resumption after timeout

### C13 — Max 20 Iterations Per Agent (OpenHands Loop)
Each agent's observe→think→act loop runs max 20 iterations.
- FinOps Agent kills at budget threshold before iteration limit if needed
- Prevents infinite loops on hard problems

### C14 — Visual Similarity Threshold ≥88%
Screenshot→code visual verify loop must achieve ≥88% similarity.
- Below 88% → agent sees diff and iterates
- Applies to SCREENSHOT mode and FIGMA mode
- **Reason:** 88% catches major visual regressions without over-constraining

---

## WHAT TO DO IF A CONSTRAINT IS CHALLENGED
1. State the constraint ID (C1–C14)
2. Explain the rationale (listed above)
3. If override genuinely needed → create DECISIONS.md entry with:
   - Why the constraint needs changing
   - New safeguards replacing it
   - Preetham's explicit approval

*v2.0 — March 2026*
