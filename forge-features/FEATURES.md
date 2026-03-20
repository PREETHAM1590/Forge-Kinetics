# FEATURES.md — Complete Feature Roadmap v2.0
> All Forge features: original + copied from Manus + inspired by Oz/ADK.
> Sorted by phase. Update status as features ship.

---

## STATUS KEY
✅ DONE | 🔄 IN PROGRESS | 📋 PLANNED | 💡 FUTURE IDEA

---

## CORE FORGE FEATURES (original — competitive moat)

| Feature | Description | Phase | Status |
|---|---|---|---|
| **15-Agent Pipeline** | PM→Architect→Build→Quality→Deploy | 1–2 | 🔄 |
| **Per-Agent Sandboxes** | Each agent owns its own E2B runtime | 1–2 | 📋 |
| **HITL Approval Gate** | Human cryptographic sign-off before deploy | 1–2 | 📋 |
| **HITL Steer Mode** | Join live session to redirect agent mid-build | 5–6 | 📋 |
| **OpenHands Runtime** | observe→think→act loop per agent (max 20 iter) | 1–2 | 📋 |
| **FinOps Agent** | Real-time token budget enforcement | 1–2 | 📋 |
| **Credit-Based Pricing** | $99/$299/Enterprise + pay-per-credit | 1–2 | 📋 |
| **Temporal Knowledge Graph** | Neo4j — client history, preferences, decisions | 3–4 | 📋 |
| **Federated Collective Brain** | Cross-project learning, differential privacy | 3–4 | 📋 |
| **Maintenance Agent** | Nightly monitor → PR proposals (never auto-applies) | 3–4 | 📋 |
| **Git Artifact Transport** | Agents commit to git, next agent pulls | 1–2 | 📋 |
| **LangGraph + ADK Hybrid** | LangGraph state + ADK Parallel/Loop/A2A/Resume | 1–2 | 📋 |

---

## FEATURES COPIED FROM MANUS

### 1. Forge Skills *(from Manus Skills)*
> Manus: static SKILL.md files. Forge: self-improving via Collective Brain.

**What it is:** Agents load a proven playbook for every common task instead of figuring it out from scratch. PM Agent → Architect maps PRD tasks → Skills → agents execute Skills.

**Progressive Disclosure:**
| Level | Content | Tokens | When |
|---|---|---|---|
| L1 Metadata | Name + description | ~100/skill | Always at startup |
| L2 Instructions | Full SKILL.md | <5k | When skill triggered |
| L3 Resources | Templates, schemas | On demand | When L2 references |

**Phase 1 Skills (10 total, 3 done):**
```
✅ skills/auth/supabase-auth.skill.md
✅ skills/payments/stripe-subscriptions.skill.md
✅ skills/ui/dashboard-layout.skill.md
⬜ skills/auth/clerk-auth.skill.md
⬜ skills/payments/stripe-one-time.skill.md
⬜ skills/ui/landing-page.skill.md
⬜ skills/ui/data-table-crud.skill.md
⬜ skills/api/rest-crud.skill.md
⬜ skills/api/webhook-handler.skill.md
⬜ skills/deploy/vercel-nextjs.skill.md
```

**Trigger:** Slash command `/skills` in Forge chat | Phase: 1–2 ✅

---

### 2. Wide Research Mode *(from Manus Wide Research)*
**What it is:** Research Agent spawns 5–10 parallel sub-agents, each investigating a different angle, then synthesizes into a comprehensive report.

**Forge use cases:**
- "Research best auth library for this stack before we build"
- "Audit all 47 npm dependencies for CVEs"
- "Analyze 10 competitor pricing pages before building ours"
- "Find all breaking changes in Next.js 15 affecting this codebase"

**Implementation:** ADK ParallelAgent running Research sub-agents simultaneously
**Phase:** 3–4

---

### 3. Scheduled Tasks *(from Manus Scheduled Tasks)*
**What it is:** BullMQ cron triggers specific agents automatically.

**Forge-specific schedules:**
```
Nightly 2 AM → Maintenance Agent scans Sentry + Uptime + Lighthouse
Every Monday → Growth Agent generates weekly performance summary
1st of month → Billing report + credit usage summary + client invoice
On Sentry alert → Maintenance Agent immediate incident analysis
On new PR → Docs Agent updates changelog
```

**Schedule types:** Daily / Weekday / Weekly / Monthly / On-Event / One-Time
**Output destinations:** Slack channel / Email / Client dashboard / Notion
**Phase:** 3–4

---

### 4. Mail Forge *(from Manus Mail Manus)*
**What it is:** Each Forge workspace gets a unique email address. Email triggers the full build pipeline.

**Workspace email addresses:**
```
[email protected]          → triggers new build
[email protected]    → HITL approval via email reply
[email protected]        → Maintenance Agent bug report
[email protected]       → weekly performance audit
```

**The agency workflow:**
1. Client emails account manager: "Add CSV export to reports page"
2. Account manager forwards to `[email protected]`
3. PM Agent reads email → generates PRD → runs pipeline
4. HITL email sent to account manager: diff + plain English summary
5. Account manager replies "APPROVE"
6. DevOps Agent deploys

**Client never touches Forge. Agency uses email they already have.**

**Security:** Approved sender whitelist per workspace
**Phase:** 5–6

---

### 5. Cloud Browser *(from Manus Cloud Browser)*
**What it is:** Upgrade from Playwright headless to a full persistent visual browser session that agents operate during their sandbox loop.

**Capabilities:**
- Navigate to `localhost:3000` after build
- Screenshots at every responsive breakpoint (320px, 768px, 1024px, 1440px)
- Click through core user flows to verify they work
- Verify auth redirects, form submissions, data persistence
- Visual regression test: compare rendered vs design spec

**Already partially in Forge:** Playwright MCP in Frontend Agent. This upgrades it.
**Phase:** 3–4

---

### 6. Browser Operator *(from Manus Browser Operator)*
**What it is:** Testing Agent operates a real browser like a human QA tester — not just running scripts, but actually using the app.

**Post-deploy smoke test flow:**
1. After HITL approval + deploy, Testing Agent opens live URL
2. Logs in with test credentials
3. Navigates through every core user flow
4. Verifies data persists, errors are handled, edge cases work
5. Records full session video for HITL review
6. If anything fails → triggers rollback before client sees it

**Phase:** 5–6

---

### 7. Forge Reports *(from Manus Slides)*
**What it is:** After every build, Docs Agent auto-generates a client-deliverable report.

**Report contents:**
- Architecture overview (what was built + why)
- Component inventory (what's in the codebase)
- API documentation (all routes + schemas)
- Deployment info (URLs, env vars needed)
- Maintenance guide (how to update content)
- Performance scores (Lighthouse results)
- Skills used (which playbooks were executed)

**Output formats:**
- PDF (send to client)
- Notion page (agency documentation)
- Markdown (developer handoff)
- Slide deck (agency presentation)

**Phase:** 3–4 (Docs Agent upgrade)

---

### 8. Forge Collab *(from Manus Collab)*
**What it is:** Multi-role team collaboration on client projects.

**Roles:**
| Role | Permissions |
|---|---|
| Owner | Full access, HITL approval authority |
| Developer | View pipeline, add comments, cannot approve deploy |
| Client | Read-only dashboard, HITL approval (if granted), feature requests |

**Client Portal** (separate lightweight view):
- Live build progress
- HITL approval requests
- Deployed app URL
- Health reports
- Feature request form → triggers Mail Forge pipeline

**Phase:** 3–4

---

### 9. Data Analysis & Visualization *(from Manus Data Analysis)*
**What it is:** Client uploads data → Growth Agent analyzes → builds visualization components INTO the app.

**Use cases:**
- "Here's our GA4 export. Add a live analytics dashboard."
- "Here's our Stripe CSV. Build a revenue chart component."
- "Here's our user data. Show a cohort analysis page."

**Stack:** pandas + numpy (analysis) + Recharts (components) → built by Frontend Agent

**Phase:** 7–9

---

### 10. Multimedia Processing *(from Manus Multimedia Processing)*
**What it is:** Multiple input modalities for starting a Forge build.

**Input types:**
| Input | Processing | Who handles |
|---|---|---|
| Voice memo / audio | Whisper → transcript → PRD | PM Agent |
| Screenshot / image | 2-pass spec extraction → code | Design Agent |
| Video of existing app | Agent watches → understands UX → rebuilds better | Design + PM Agent |
| PDF / Word doc | Text extraction → PRD | PM Agent |
| Figma URL | MCP exact tokens → code | Design Agent |
| Email | Text analysis → PRD | PM Agent via Mail Forge |

**Phase:** 7–9

---

## FORGE-ONLY FEATURES (no Manus/Oz equivalent)

| Feature | Why competitors can't copy |
|---|---|
| **Temporal Knowledge Graph** | Requires years of client history — can't fake it |
| **Federated Collective Brain** | Needs 1000s of projects for network effect |
| **15 Specialized Agents** | Competitors use 1 general agent |
| **HITL Gate (mandatory)** | Manus/Lovable have no production safety |
| **Agency white-label** | Manus is consumer, not B2B |
| **Skills self-improvement** | Collective Brain feeds back into Skills |
| **Post-deploy Maintenance** | Nobody else has ongoing monitoring + PR proposals |

---

## PHASED FEATURE DELIVERY SUMMARY

| Phase | Key features shipping |
|---|---|
| **1–2** | Core pipeline, Forge Skills v1, FinOps, HITL gate, per-agent sandboxes |
| **3–4** | Knowledge Graph, Maintenance scheduled, Forge Reports, Cloud Browser, Collab, Wide Research |
| **5–6** | Mail Forge, Browser Operator, HITL Steer Mode, Security/Testing/Critic agents |
| **7–9** | Data Analysis, Multimedia (voice/video→app), second stack, ML Agent |
| **10–12** | Skills self-improvement, marketplace, white-label, public API |

*v2.0 — March 2026*
