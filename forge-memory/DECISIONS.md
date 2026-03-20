# DECISIONS.md — Architectural Decision Log v2.0
> All major decisions logged with rationale. DO NOT re-debate these.
> To override a decision, add a new entry superseding the old one.

---

### DECISION-001: Credit-Based Pricing
- **Date:** March 2026
- **Decision:** $99 Studio (500 credits) / $299 Agency (2,000 credits) / Enterprise custom. 1 credit = $0.05 compute. Overage = pay-as-you-go.
- **Rationale:** Single complex build costs $10–40 in LLM API fees. Multi-agent token consumption is multiplicative. Flat-rate at $29/month → guaranteed negative margin on any real usage.
- **Alternatives:** Flat-rate unlimited, pure usage-based, per-seat
- **Status:** ACTIVE

---

### DECISION-002: Technical Agencies as Primary Target
- **Date:** March 2026
- **Decision:** Target technical agencies, dev shops, freelancers. NOT non-developers.
- **Rationale:** Non-developers can't audit AI output → panic on edge cases → churn. All 3 research reports explicitly warn against mixed targeting. Technical users can evaluate output, bill $15k/project, will pay $299/month.
- **Alternatives:** Consumer market, SMBs, non-developers
- **Status:** ACTIVE

---

### DECISION-003: Next.js + Supabase Scope Lock (Phase 1)
- **Date:** March 2026
- **Decision:** Phase 1 builds Next.js + Supabase apps ONLY.
- **Rationale:** SWE-bench Pro: 20–40% success on complex multi-stack tasks. Scope lock → 90%+ success on one stack. Own it deeply before expanding.
- **Second stack:** T3 Stack or React + Firebase — Month 7–9
- **Status:** ACTIVE

---

### DECISION-004: HITL Gate Mandatory
- **Date:** March 2026
- **Decision:** Every production deployment requires explicit human approval. No exceptions. DevOps Agent blocked until it receives a valid cryptographic HITL approval token.
- **Rationale:** AI-generated code has OWASP Top 10 vulns in 45% of tasks. EU AI Act 2026. Legal liability for autonomous deploys. Also a product feature: "you're always in control."
- **Status:** ACTIVE

---

### DECISION-005: Per-Agent E2B Sandboxes
- **Date:** March 2026
- **Decision:** Each build agent owns its own purpose-specific E2B sandbox. No shared sandbox. No execution on host machine. Ever.
- **Rationale:** True isolation prevents race conditions (agents writing to shared filesystem). Right-sized environments (Frontend gets Node, Backend gets Python). Parallel execution is trivial. Full audit trail per agent.
- **Alternatives:** Shared sandbox, Docker locally, no sandbox
- **Status:** ACTIVE (upgraded from shared E2B to per-agent)

---

### DECISION-006: LangGraph for Master Orchestration
- **Date:** March 2026
- **Decision:** LangGraph owns the master ForgeState graph, routing, checkpointing, and LangSmith observability.
- **Rationale:** Stateful workflows with Pydantic state, built-in checkpointing, cyclic graph support, native LangSmith integration, production-grade persistence.
- **Alternatives:** AutoGen (no native persistence), CrewAI (too opinionated), custom orchestrator
- **Status:** ACTIVE

---

### DECISION-007: Neo4j for Temporal Knowledge Graph
- **Date:** March 2026
- **Decision:** Neo4j with Graphiti for the Temporal Knowledge Graph (Tier 5 memory).
- **Rationale:** Graph DB is the only efficient structure for relationship queries. Graphiti provides agent-native interface. PostgreSQL + JSONB insufficient for complex relationship traversal.
- **Alternatives:** PostgreSQL + JSONB, Redis Graph, Amazon Neptune
- **Status:** ACTIVE

---

### DECISION-008: PydanticAI for All Agent Output Validation
- **Date:** March 2026
- **Decision:** Every agent output validated against a Pydantic schema before passing downstream.
- **Rationale:** MAST taxonomy: 37% of multi-agent failures from inter-agent misalignment. Schema validation at every boundary eliminates type errors propagating.
- **Retry logic:** FAIL → retry max 3 → Critic escalation → human escalation
- **Status:** ACTIVE

---

### DECISION-009: Maintenance Agent Monitor-Only
- **Date:** March 2026
- **Decision:** Maintenance Agent creates draft PRs only. Never applies patches autonomously.
- **Rationale:** EU AI Act compliance. Production stability. User control. "Monitors and proposes" is also a better product story than "auto-patches."
- **Status:** ACTIVE

---

### DECISION-010: Federated Learning for Collective Brain
- **Date:** March 2026
- **Decision:** Collective Brain uses Federated Learning — only encrypted parameter updates cross tenant boundaries. No raw code, no prompts, no project data shared.
- **Rationale:** GDPR Art. 5 data minimization. Sharing raw code = legal liability. Federated Learning + Differential Privacy achieves network effect without privacy violation.
- **Status:** ACTIVE

---

### DECISION-011: Hybrid LangGraph + Google ADK
- **Date:** March 2026
- **Decision:** Use both LangGraph and Google ADK. LangGraph owns the master state graph. ADK provides workflow patterns and protocols.
- **Rationale:** ADK's ParallelAgent is cleaner than manual LangGraph wiring for Frontend∥Backend. ADK's LoopAgent is perfect for Testing Agent retry. ADK's Resume solves HITL gate without custom build. A2A is Google's open standard for agent discovery. LangGraph still owns state, routing, LangSmith.
- **Split:** LangGraph = state/routing/observability. ADK = Parallel/Loop/Resume/A2A.
- **Alternatives:** LangGraph only (more manual work), ADK only (less LangSmith integration), AutoGen
- **Status:** ACTIVE

---

### DECISION-012: 2-Pass Screenshot→Code Pipeline
- **Date:** March 2026
- **Decision:** Screenshot-to-code uses a strict 2-pass pipeline: Pass 1 = vision model extracts full spec (no code), Pass 2 = code model builds from spec (no vision), Pass 3 = visual verify loop ≥88% similarity.
- **Rationale:** Single-pass mixing analysis + generation loses detail. Separating concerns: vision model focuses 100% on extracting, code model focuses 100% on building. Visual verify loop catches remaining gaps.
- **Threshold:** 88% visual similarity (Playwright screenshot comparison)
- **Modes:** FIGMA mode (exact tokens via MCP), SCREENSHOT mode (2-pass + verify), PRD_ONLY mode (Design Agent generates wireframe first)
- **Status:** ACTIVE

---

### DECISION-013: Progressive Disclosure Skills System
- **Date:** March 2026
- **Decision:** Forge implements a SKILL.md-based library with progressive disclosure (copied from Manus, upgraded with Collective Brain self-improvement).
- **Rationale:** Manus Skills proved the pattern works (97% diff acceptance rate). Progressive disclosure solves context window problem: load ALL skill metadata (~100 tokens each) at startup, load full instructions only when triggered. Forge advantage: skills improve with every real build via Collective Brain.
- **Levels:** L1 metadata (always), L2 instructions (on trigger), L3 resources (on demand)
- **Self-improvement:** Every successful build anonymously contributes to Collective Brain notes in the relevant skill
- **Status:** ACTIVE

---

### DECISION-014: OpenHands-Style Agent Runtime
- **Date:** March 2026
- **Decision:** All build agents use an observe→think→act loop (OpenHands pattern) inside their own E2B sandbox. Max 20 iterations per agent. FinOps kills at budget.
- **Rationale:** One-shot code generation fails on complex tasks. The agent iterates: writes code → runs build → sees errors → fixes → repeats. Like a human developer at a terminal. This is why OpenHands gets dramatically better results than prompt-and-pray approaches.
- **Key difference from OpenHands:** Forge has 15 specialized agents each with their own sandbox, vs OpenHands' single general agent.
- **Status:** ACTIVE

*v2.0 — March 2026*
