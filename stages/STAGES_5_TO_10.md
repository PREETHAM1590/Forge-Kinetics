# FORGE — STAGES 5–10 PROMPTS
# ================================================
# Each stage builds on the previous.
# Copy the relevant stage section when you start that stage.
# ================================================

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STAGE 5: HITL Gate + DevOps Agent + Real Deploy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## PREREQUISITE: Stages 1–4 complete

## WHAT YOU ARE BUILDING
The HITL (Human-in-the-Loop) approval gate and DevOps Agent.
Nothing deploys without a human cryptographic sign-off.

## FILES TO CREATE

### forge/hitl/gate.py
```python
import hashlib, secrets, json
from datetime import datetime
from forge.core.state import ForgeState
from forge.sandbox.git_transport import get_diff_summary

class HITLGate:
    """ADK Resume pattern — pause pipeline, wait for human, resume."""

    async def build_payload(self, state: ForgeState) -> dict:
        """Build the payload shown to the human reviewer."""
        diff = await get_diff_summary(...)
        return {
            "project_id": state.project_id,
            "project_name": state.prd.project_name,
            "critic_summary": state.critic_verdict.summary,
            "risk_level": state.critic_verdict.risk_level,
            "security_status": state.security_report.verdict,
            "test_coverage": state.test_results.coverage_percent,
            "rollback_plan": state.critic_verdict.rollback_plan,
            "diff_summary": diff,
            "timestamp": datetime.utcnow().isoformat(),
        }

    async def pause_for_approval(self, state: ForgeState) -> ForgeState:
        """Pause pipeline. Send notification. Wait for token."""
        payload = await self.build_payload(state)
        state.hitl_status = "pending"
        state.pipeline_status = "paused"
        # In production: send to dashboard + email notification
        print(f"\n{'='*60}")
        print(f"⏸  HITL GATE — Human Approval Required")
        print(f"   Project: {payload['project_name']}")
        print(f"   Risk: {payload['risk_level'].upper()}")
        print(f"   Security: {payload['security_status']}")
        print(f"   Test Coverage: {payload['test_coverage']}%")
        print(f"   Summary: {payload['critic_summary'][:100]}")
        print(f"\n   To approve: call approve(project_id, approver_id)")
        print(f"{'='*60}\n")
        return state

    def generate_approval_token(self, project_id: str, approver_id: str) -> str:
        """Generate cryptographic approval token."""
        timestamp = datetime.utcnow().isoformat()
        payload = f"{project_id}:{approver_id}:{timestamp}"
        token = hashlib.sha256(f"{payload}:{secrets.token_hex(32)}".encode()).hexdigest()
        return token

    def verify_token(self, token: str, project_id: str) -> bool:
        """Verify approval token is valid."""
        return bool(token) and len(token) == 64  # simplified — use JWT in production
```

### forge/agents/devops.py
```python
import os, httpx
from forge.agents.base import BaseAgent
from forge.core.state import ForgeState
from forge.sandbox.e2b_runtime import AgentSandbox
from forge.hitl.gate import HITLGate

VERCEL_API = "https://api.vercel.com"

class DevOpsAgent(BaseAgent):
    name = "devops"
    max_iterations = 5
    sandbox_image = "alpine-with-cli"

    async def run(self, state: ForgeState) -> ForgeState:
        # HARD RULE C1: verify HITL token BEFORE anything else
        gate = HITLGate()
        if not state.hitl_approval_token:
            raise ValueError("BLOCKED: No HITL approval token. Cannot deploy.")
        if not gate.verify_token(state.hitl_approval_token, state.project_id):
            raise ValueError("BLOCKED: Invalid HITL approval token.")

        print(f"✓ HITL token verified. Starting deployment...")
        async with AgentSandbox(self.name, template="base") as sandbox:
            self.sandbox = sandbox
            await sandbox.run_bash(
                "npm install -g vercel railway"
            )
            return await super().run(state)

    async def observe(self, state: ForgeState) -> dict:
        return {
            "project_path": state.frontend_code.get("project_path", "") if state.frontend_code else "",
            "env_vars": state.tech_spec.env_vars_needed if state.tech_spec else [],
            "iteration": state.iteration_count,
        }

    async def think(self, observation: dict, state: ForgeState) -> dict:
        return {"action": "deploy_to_vercel", "obs": observation}

    async def act(self, action: dict, state: ForgeState) -> dict:
        obs = action["obs"]
        # Deploy to Vercel via API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{VERCEL_API}/v13/deployments",
                headers={"Authorization": f"Bearer {os.getenv('VERCEL_TOKEN')}"},
                json={
                    "name": f"forge-{state.project_id[:8]}",
                    "target": "production",
                },
                timeout=60,
            )
            if response.status_code != 200:
                return {"task_complete": False, "error": response.text}

            deploy_data = response.json()
            deploy_url = f"https://{deploy_data.get('url', 'pending.vercel.app')}"
            return {"task_complete": True, "deploy_url": deploy_url}

    async def on_complete(self, result: dict, state: ForgeState) -> ForgeState:
        state.deploy_url = result.get("deploy_url", "https://deployed.vercel.app")
        state.pipeline_status = "completed"
        print(f"✓ DevOps Agent: Deployed → {state.deploy_url}")
        return state
```

### platform/app/(app)/hitl/[projectId]/page.tsx
```typescript
// HITL approval dashboard — what the human sees
import { HITLApprovalCard } from "@/components/hitl/approval-card"

export default async function HITLPage({ params }: { params: { projectId: string } }) {
  // Fetch HITL payload for this project
  const payload = await getHITLPayload(params.projectId)

  return (
    <div className="max-w-4xl mx-auto p-8">
      <h1 className="text-2xl font-bold mb-6">Review & Approve Deployment</h1>
      <HITLApprovalCard
        projectName={payload.projectName}
        riskLevel={payload.riskLevel}
        criticSummary={payload.criticSummary}
        securityStatus={payload.securityStatus}
        testCoverage={payload.testCoverage}
        diffSummary={payload.diffSummary}
        rollbackPlan={payload.rollbackPlan}
        onApprove={(approverId) => approveDeployment(params.projectId, approverId)}
        onReject={(reason) => rejectDeployment(params.projectId, reason)}
        onSteer={() => joinLiveSession(params.projectId)}
      />
    </div>
  )
}
```

## VALIDATION — Stage 5 is DONE when:
- [ ] DevOps Agent refuses to run without valid HITL token
- [ ] HITL gate shows correct summary in console/dashboard
- [ ] Approval token is generated and verified
- [ ] Real Vercel deployment happens after approval
- [ ] Deploy URL is captured in ForgeState
- [ ] Pipeline status → "completed" after deploy

## AFTER COMPLETING STAGE 5
`git commit -m "feat(stage-5): HITL gate + DevOps agent + Vercel deploy"`


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STAGE 6: Memory + RAG + Knowledge Graph
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## PREREQUISITE: Stage 5 complete (full deploy pipeline working)

## WHAT YOU ARE BUILDING
The 5-tier memory system: Core, Recall (Redis), Archival (ChromaDB + Pinecone),
Log (/memory/ folder), and Temporal Knowledge Graph (Neo4j).

## FILES TO CREATE

### forge/memory/knowledge_graph.py
```python
from neo4j import AsyncGraphDatabase
from graphiti_core import Graphiti
from typing import Any

class TemporalKnowledgeGraph:
    """Tier 5 memory — stores client preferences, decisions, constraints.
    Queried by every agent before any action.
    Core of Brand Memory defensibility.
    """

    def __init__(self, uri: str, user: str, password: str):
        self.driver = AsyncGraphDatabase.driver(uri, auth=(user, password))
        self.graphiti = Graphiti(uri, user, password)

    async def store_decision(self, project_id: str, decision: dict):
        """Store an architectural decision for this client."""
        async with self.driver.session() as session:
            await session.run(
                """MERGE (p:Project {id: $project_id})
                   CREATE (d:Decision {
                     id: randomUUID(),
                     type: $type,
                     value: $value,
                     timestamp: datetime()
                   })
                   MERGE (p)-[:HAS_DECISION]->(d)""",
                project_id=project_id, **decision
            )

    async def get_client_context(self, project_id: str) -> dict:
        """Get all stored preferences and decisions for a client.
        Called by Architect before designing any spec.
        """
        async with self.driver.session() as session:
            result = await session.run(
                """MATCH (p:Project {id: $project_id})-[:HAS_DECISION]->(d)
                   RETURN d ORDER BY d.timestamp DESC LIMIT 50""",
                project_id=project_id
            )
            records = await result.data()
            return {
                "past_decisions": records,
                "project_id": project_id,
            }

    async def store_brand_memory(self, project_id: str, brand: dict):
        """Store brand colors, fonts, conventions."""
        async with self.driver.session() as session:
            await session.run(
                """MERGE (p:Project {id: $project_id})
                   SET p.brand_colors = $colors,
                       p.font_family = $font,
                       p.conventions = $conventions""",
                project_id=project_id, **brand
            )
```

### forge/memory/recall.py
```python
import redis.asyncio as redis
from mem0 import MemoryClient
import json

class RecallMemory:
    """Tier 2 — recent session history. Redis + Mem0."""

    def __init__(self, redis_url: str, mem0_api_key: str):
        self.redis = redis.from_url(redis_url)
        self.mem0 = MemoryClient(api_key=mem0_api_key)

    async def store_session(self, session_id: str, summary: str, user_id: str):
        """Store what happened in this session."""
        await self.redis.setex(
            f"session:{session_id}",
            60 * 60 * 24 * 30,  # 30 days TTL
            json.dumps({"summary": summary, "user_id": user_id})
        )
        await self.mem0.add(
            messages=[{"role": "system", "content": summary}],
            user_id=user_id,
        )

    async def get_recent_context(self, user_id: str) -> str:
        """Get recent context for this user."""
        memories = await self.mem0.search(
            query="recent project decisions",
            user_id=user_id,
            limit=10,
        )
        return "\n".join(m["memory"] for m in memories.get("results", []))
```

### forge/rag/codebase.py
```python
import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from pathlib import Path

class CodebaseRAG:
    """Per-project codebase RAG. Code-aware chunking."""

    def __init__(self, project_id: str):
        self.project_id = project_id
        self.client = chromadb.PersistentClient(path=f"/data/chroma/{project_id}")
        self.collection = self.client.get_or_create_collection(f"codebase_{project_id}")

    async def index_codebase(self, project_path: str):
        """Index a project's codebase for semantic search."""
        documents = SimpleDirectoryReader(
            project_path,
            required_exts=[".ts", ".tsx", ".py", ".sql", ".md"],
            recursive=True,
        ).load_data()
        store = ChromaVectorStore(chroma_collection=self.collection)
        self.index = VectorStoreIndex.from_documents(documents, vector_store=store)

    async def search(self, query: str, top_k: int = 5) -> list[str]:
        """Search codebase for relevant files/functions."""
        retriever = self.index.as_retriever(similarity_top_k=top_k)
        nodes = retriever.retrieve(query)
        return [n.text for n in nodes]
```

## VALIDATION — Stage 6 is DONE when:
- [ ] Neo4j stores and retrieves client decisions
- [ ] Architect queries Knowledge Graph before every design
- [ ] Codebase RAG indexes built project files
- [ ] Recall Memory stores session summaries in Redis
- [ ] Skills loader uses ChromaDB metadata

`git commit -m "feat(stage-6): 5-tier memory system + Knowledge Graph + RAG pipelines"`


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STAGE 7: Platform UI (Next.js Dashboard)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## PREREQUISITE: Stage 6 complete

## WHAT YOU ARE BUILDING
The Forge platform itself — the Next.js 15 dashboard that agencies use.
Use the Skills files to build it. Forge builds itself using its own patterns.

## PAGES TO BUILD (use the Skills)

### Use dashboard-layout.skill.md:
- `platform/app/(app)/layout.tsx` — main app shell

### Use landing-page.skill.md:
- `platform/app/(marketing)/page.tsx` — Forge marketing homepage
  Hero: "Your AI Software Agency"
  Features: 15 Agents, Knowledge Graph, HITL Gate
  Pricing: Studio $99 / Agency $299 / Enterprise

### Use clerk-auth.skill.md:
- `platform/app/sign-in/[[...sign-in]]/page.tsx`
- `platform/app/sign-up/[[...sign-up]]/page.tsx`

### Use stripe-subscriptions.skill.md:
- `platform/app/(app)/billing/page.tsx`

### Build from scratch:
```typescript
// platform/app/(app)/dashboard/page.tsx
// Show: active projects, recent builds, credit balance, quick start

// platform/app/(app)/projects/[id]/page.tsx
// Show: live pipeline progress, agent status, HITL gate, deploy URL

// platform/app/(app)/projects/[id]/hitl/page.tsx
// HITL approval dashboard — diff + plain English + approve/reject/steer buttons

// platform/app/(app)/settings/page.tsx
// Workspace settings, team members, connected integrations
```

### platform/components/pipeline/agent-status.tsx
```typescript
"use client"
// Real-time pipeline visualization
// Shows each of 15 agents: waiting | running | complete | failed
// Updates via Supabase realtime subscription
export function PipelineStatus({ projectId }: { projectId: string }) {
  // Subscribe to forge_pipeline_events table
  // Show agent cards with status indicators
}
```

## VALIDATION — Stage 7 is DONE when:
- [ ] Landing page renders with pricing
- [ ] Auth works (sign up → dashboard)
- [ ] New project form → triggers Forge pipeline
- [ ] Pipeline visualization shows agent progress in real-time
- [ ] HITL gate page shows diff + approve/reject buttons
- [ ] Billing page shows current plan + credit balance
- [ ] Stripe checkout works end-to-end
- [ ] Lighthouse score ≥85

`git commit -m "feat(stage-7): platform UI — dashboard + HITL gate + billing"`


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STAGE 8: Supporting Agents (FinOps + Research + Maintenance + Docs)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## PREREQUISITE: Stage 7 complete

## WHAT YOU ARE BUILDING
The 4 supporting agents that run alongside or after the main pipeline.

### forge/agents/finops.py
```python
"""FinOps Agent — runs as async sidecar, enforces token budgets.
Kills runaway agents when budget is exceeded. Never lets the platform
go bankrupt from a single misbehaving build."""

class FinOpsAgent:
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

    async def record_usage(self, agent_name: str, tokens: int, state: ForgeState):
        """Record token usage. Kill agent if budget exceeded."""
        state.token_budget.per_agent[agent_name] = (
            state.token_budget.per_agent.get(agent_name, 0) + tokens
        )
        state.token_budget.total_used += tokens
        budget = self.DEFAULT_BUDGETS.get(agent_name, 50_000)
        if state.token_budget.per_agent[agent_name] > budget:
            state.token_budget.is_exceeded = True
            raise BudgetExceededError(
                f"{agent_name} used {state.token_budget.per_agent[agent_name]} tokens "
                f"(budget: {budget}). Pipeline paused."
            )

    def get_cost_report(self, state: ForgeState) -> dict:
        """Show what each build actually cost."""
        cost_per_token = 0.000005  # $5 per 1M = $0.000005 per token
        return {
            "total_tokens": state.token_budget.total_used,
            "total_cost_usd": round(state.token_budget.total_used * cost_per_token, 4),
            "credits_used": max(1, state.token_budget.total_used // 10_000),
            "per_agent": {
                k: {"tokens": v, "cost_usd": round(v * cost_per_token, 4)}
                for k, v in state.token_budget.per_agent.items()
            }
        }
```

### forge/agents/maintenance.py
```python
"""Maintenance Agent — runs on schedule (nightly via BullMQ).
Monitors production apps. Proposes PRs. NEVER auto-applies.
Rule C7: monitor only."""

import httpx
from datetime import datetime

class MaintenanceAgent:
    async def run_nightly_scan(self, project_id: str, deploy_url: str) -> dict:
        """Nightly: check Sentry, Uptime, Lighthouse. Propose PRs if issues found."""
        sentry_issues = await self._check_sentry(project_id)
        uptime_status = await self._check_uptime(deploy_url)
        lighthouse = await self._run_lighthouse(deploy_url)
        issues_found = []
        if sentry_issues:
            issues_found.append(f"{len(sentry_issues)} new Sentry errors")
        if lighthouse.get("performance", 100) < 70:
            issues_found.append(f"Lighthouse performance: {lighthouse['performance']}")
        if issues_found:
            # Create draft PR proposal — NEVER auto-merge
            return {
                "has_issues": True,
                "issues": issues_found,
                "pr_title": f"Maintenance: {', '.join(issues_found[:2])}",
                "pr_body": self._generate_pr_body(sentry_issues, lighthouse),
                "status": "draft_pr_created",
                "auto_applied": False,  # ALWAYS false
            }
        return {"has_issues": False, "status": "healthy"}

    async def _check_sentry(self, project_id: str) -> list:
        """Query Sentry for new issues in the last 24 hours."""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"https://sentry.io/api/0/projects/{project_id}/issues/",
                headers={"Authorization": f"Bearer {os.getenv('SENTRY_TOKEN')}"},
                params={"query": "is:unresolved age:-24h"},
            )
            return resp.json() if resp.status_code == 200 else []
```

### forge/agents/docs.py
```python
"""Docs Agent — triggered on every git commit. Auto-generates docs."""

class DocsAgent:
    async def generate_on_commit(self, state: ForgeState, diff: str) -> str:
        """Generate or update docs based on what changed in this commit."""
        prompt = f"""Diff:
{diff[:3000]}

Generate/update:
1. API route documentation (if routes changed)
2. Component documentation (if components changed)
3. CHANGELOG entry (always)
4. Architecture notes (if major structural change)

Output structured markdown."""
        message = await self.client.messages.create(
            model="claude-haiku-4-5",  # Cheapest — docs don't need Opus
            max_tokens=2048,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
```

### forge/finops/scheduler.py (BullMQ setup)
```python
"""Schedule nightly maintenance scans for all deployed projects."""
from bullmq import Queue, Worker
import asyncio

maintenance_queue = Queue("maintenance", connection={"host": "localhost", "port": 6379})

async def schedule_nightly_scans(deployed_projects: list[dict]):
    """Add all deployed projects to nightly maintenance queue."""
    for project in deployed_projects:
        await maintenance_queue.add(
            "nightly_scan",
            {"project_id": project["id"], "deploy_url": project["url"]},
            {"delay": 0, "repeat": {"cron": "0 2 * * *"}}  # 2 AM every night
        )
```

## VALIDATION — Stage 8 is DONE when:
- [ ] FinOps Agent kills a test agent when budget exceeded
- [ ] Cost report shows token usage per agent
- [ ] Maintenance Agent runs scan and creates draft PR (never auto-applies)
- [ ] BullMQ cron schedules nightly scans
- [ ] Docs Agent generates changelog on commit

`git commit -m "feat(stage-8): FinOps + Maintenance + Docs + Research agents"`


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STAGE 9: Manus-Inspired Features
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## PREREQUISITE: Stage 8 complete

## WHAT YOU ARE BUILDING
Features copied from Manus and upgraded for Forge's context.
See forge-features/FEATURES.md for full specs.

## FEATURES TO BUILD (in priority order)

### 1. Scheduled Tasks
```python
# forge/scheduler/tasks.py
# Add to BullMQ alongside nightly maintenance
SCHEDULED_TASKS = [
    {"name": "nightly_maintenance", "cron": "0 2 * * *", "agent": "maintenance"},
    {"name": "weekly_report", "cron": "0 9 * * 1", "agent": "docs"},  # Monday 9AM
    {"name": "monthly_billing", "cron": "0 9 1 * *", "agent": "finops"},  # 1st of month
]
```

### 2. Mail Forge
```python
# forge/mail/receiver.py
# Each workspace gets a unique email: abc123@builds.forge.dev
# Incoming email → PM Agent reads it → triggers pipeline
# HITL approval via email reply

class MailForgeReceiver:
    async def process_inbound(self, email: dict):
        """Receive email → extract intent → trigger PM Agent."""
        sender = email["from"]
        subject = email["subject"]
        body = email["body"]
        # Verify sender is in approved_senders list
        # Extract task from email body
        # Create ForgeState with input_type="email"
        # Start pipeline
```

### 3. Wide Research Mode
```python
# forge/agents/research.py — upgrade to parallel sub-agents
from google.adk.agents import ParallelAgent

class WideResearchMode:
    """Spawn 5-10 parallel Research sub-agents for deep investigation."""

    async def research(self, main_query: str, depth: int = 5) -> str:
        sub_queries = self._decompose_query(main_query, n=depth)
        parallel = ParallelAgent(
            sub_agents=[ResearchSubAgent(q) for q in sub_queries]
        )
        results = await parallel.run({})
        return self._synthesize(results)

    def _decompose_query(self, query: str, n: int) -> list[str]:
        """Break one query into n parallel sub-queries."""
        # E.g. "audit npm deps for CVEs" → 
        # ["check auth deps", "check payment deps", "check build deps", ...]
```

### 4. 2-Pass Screenshot→Code Pipeline
```python
# forge/agents/design.py — full implementation

SPEC_EXTRACTION_PROMPT = """Analyze this screenshot. Extract EVERY measurable value.
Output structured spec with:
- Layout: flex/grid pattern, max-width, spacing grid (4px or 8px base)
- Colors: exact hex for EVERY distinct color, with description of where used
- Typography: each text style — size estimate, weight, color, letter-spacing
- Components: list every UI element with its properties
- Spacing: padding inside components, gaps between, margins
- Borders: radius values, border styles, shadows
- What you CANNOT determine: list ambiguous things + suggest reasonable defaults
Output ONLY the spec. No code. No explanation."""

class DesignAgent(BaseAgent):
    async def extract_spec_from_screenshot(self, image_bytes: bytes) -> dict:
        """Pass 1: Vision model extracts ONLY spec from screenshot."""
        response = await self.gemini.generate_content([
            SPEC_EXTRACTION_PROMPT,
            {"mime_type": "image/png", "data": image_bytes}
        ])
        return {"spec": response.text, "pass": 1}

    async def build_from_spec(self, spec: dict) -> str:
        """Pass 2: Code model builds ONLY from spec — no vision."""
        prompt = f"""Build this UI in Next.js + Tailwind.
Use EXACTLY these values — do not invent anything:
{spec['spec']}

Rules:
- Exact hex colors from spec
- Exact pixel values from spec
- Use Tailwind utility classes where possible, inline styles for exact values not in Tailwind"""
        # Claude Sonnet builds from the spec
        response = await self.claude.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=8096,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text

    async def visual_verify(self, original_image: bytes, rendered_url: str) -> float:
        """Pass 3: Compare rendered output vs original screenshot."""
        rendered = await self.browser.screenshot(rendered_url)
        similarity = await self.compare_images(original_image, rendered)
        return similarity  # target ≥0.88
```

## VALIDATION — Stage 9 is DONE when:
- [ ] Scheduled Tasks run on cron schedule
- [ ] Mail Forge receives email and triggers PM Agent
- [ ] Wide Research spawns parallel sub-agents
- [ ] Screenshot→Code produces 88%+ visual match
- [ ] All features tested end-to-end

`git commit -m "feat(stage-9): scheduled tasks + mail trigger + wide research + 2-pass design"`


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# STAGE 10: Scale — Federated Collective Brain + Public API
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## PREREQUISITE: Stage 9 complete. 10+ real projects built.

## WHAT YOU ARE BUILDING
The Collective Brain network effect moat, Skills self-improvement,
white-label platform, and public API for agencies.

### forge/rag/collective_brain.py
```python
"""Federated Collective Brain — the network effect moat.
Key rule: ONLY encrypted parameter updates cross tenant boundaries.
No raw code. No prompts. No project data. GDPR Art. 5 compliant.
"""

import numpy as np
from forge.rag.differential_privacy import add_noise

class CollectiveBrain:
    def contribute_build_patterns(self, project_id: str, patterns: dict):
        """After successful build, extract anonymous patterns.
        Apply differential privacy noise before storing.
        Rule C8: No raw code, no identifiable data crosses boundaries.
        """
        anonymous_patterns = self._anonymize(patterns)
        noisy_embedding = add_noise(
            anonymous_patterns["embedding"],
            epsilon=1.0,  # DP budget
            sensitivity=1.0
        )
        # Store anonymized, noisy embedding in Pinecone
        self.pinecone.upsert([{
            "id": f"pattern_{project_id[:8]}_{hash(str(patterns))}",
            "values": noisy_embedding.tolist(),
            "metadata": {
                "category": patterns.get("category"),
                "stack": "nextjs-supabase",
                "success": True,
                # NO project_id, NO user data, NO code content
            }
        }])

    def update_skill(self, skill_id: str, fix: dict):
        """When a real build fixes an error, add it to the skill.
        This is how Skills self-improve over time.
        """
        skill_path = f"forge-features/skills/**/{skill_id}.skill.md"
        # Append to "Collective Brain Notes" section of skill file
        new_note = f"- [{fix['error_type']}]: {fix['fix_description']}"
        # Update skill file with the anonymized fix
```

### platform/app/api/v1/[...route]/route.ts
```typescript
// Public API for agencies to trigger Forge programmatically
// Agencies can start builds, check status, approve HITL from their own tools

// POST /api/v1/projects — start a new build
// GET  /api/v1/projects/:id — get build status
// POST /api/v1/projects/:id/approve — HITL approval
// GET  /api/v1/projects/:id/logs — stream agent logs
// POST /api/v1/webhooks — register webhook for build events
```

### forge/platform/white_label.py
```python
"""White-label support for Agency tier ($299/month).
Agency's clients see their brand, not Forge.
"""

class WhiteLabelConfig:
    agency_id: str
    custom_domain: str        # clients.theiragency.com
    brand_logo_url: str
    brand_colors: dict        # {"primary": "#...", "accent": "#..."}
    custom_email_from: str    # forge@theiragency.com
    hide_forge_branding: bool = True
```

## VALIDATION — Stage 10 is DONE when:
- [ ] Collective Brain stores anonymized patterns from real builds
- [ ] Skills self-improve: new errors + fixes added to Collective Brain notes
- [ ] Public API returns correct build status
- [ ] Webhook fires on build completion
- [ ] White-label config applies custom branding
- [ ] 5 real agencies are using the platform

## FINAL COMMIT
`git commit -m "feat(stage-10): Collective Brain + Skills self-improvement + public API + white-label"`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HOW TO UPDATE AFTER EVERY STAGE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After completing ANY stage, do these 5 things:

1. FORGE_CODING_PROMPT.md → CURRENT STAGE section:
   STATUS: IN PROGRESS → STATUS: DONE
   Update CURRENTLY BUILDING to next stage

2. forge-memory/NOW.md:
   Update "Last Session Summary"
   Update "Next step"

3. forge-memory/PROJECT_INDEX.md:
   Move completed milestones from ⬜ → ✅

4. forge-memory/ROADMAP.md:
   Mark completed month milestones as ✅

5. Git commit with stage message (shown at bottom of each stage)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# QUICK REFERENCE — ALL 10 STAGES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Stage | What it builds | Key file | Commit msg |
|---|---|---|---|
| 1 | ForgeState + LangGraph + stubs | state.py | feat(stage-1): core scaffold |
| 2 | PM + Architect (real LLM) | pm_agent.py | feat(stage-2): real PM + Architect |
| 3 | Frontend + Backend + E2B | e2b_runtime.py | feat(stage-3): build agents + sandboxes |
| 4 | Security + Testing + Critic | critic.py | feat(stage-4): quality agents |
| 5 | HITL gate + DevOps + Deploy | gate.py | feat(stage-5): HITL + Vercel deploy |
| 6 | Memory + Knowledge Graph | knowledge_graph.py | feat(stage-6): memory + RAG |
| 7 | Platform UI (Next.js) | platform/app/ | feat(stage-7): platform dashboard |
| 8 | FinOps + Maintenance + Docs | finops.py | feat(stage-8): supporting agents |
| 9 | Manus features (mail, research) | design.py | feat(stage-9): Manus features |
| 10 | Collective Brain + public API | collective_brain.py | feat(stage-10): scale + moat |

*All Stages — Forge v2.0 — March 2026*
