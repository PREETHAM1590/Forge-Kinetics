# FORGE — STAGE 2 PROMPT: PM Agent + Architect Agent (Real LLM)
# ================================================
# Prerequisites: Stage 1 complete (stubs working)
# Goal: Replace stubs with real Claude Sonnet / Opus calls
# ================================================

## WHAT YOU ARE BUILDING
Replace the Stage 1 stubs with real LLM-powered agents:
- PM Agent: Claude Sonnet 4.5 → turns ANY user input into a structured PRDSchema
- Architect Agent: Claude Opus 4.5 → turns PRD into TechSpecSchema + maps tasks to Skills

## FILES TO READ FIRST
- forge-memory/AGENTS.md → PM Agent and Architect Agent specs
- forge-memory/API_CONTRACTS.md → PRDSchema and TechSpecSchema
- forge-features/FEATURES.md → Skills progressive disclosure
- forge-features/skills/ → all 11 skill files (Architect maps tasks to these)

## STAGE 2 GOAL
End state: user types "Build a SaaS dashboard with auth and Stripe" →
PM Agent returns valid PRDSchema → Architect returns TechSpecSchema with
skill_assignments mapping each feature to the right skill file.

## FILES TO CREATE / MODIFY

### 1. forge/agents/pm_agent.py (REPLACE STUB)
```python
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from forge.agents.base import BaseAgent
from forge.core.state import ForgeState, PRDSchema
from forge.skills.loader import SkillLoader
import json

SYSTEM_PROMPT = """You are the PM Agent for Forge, an AI software development platform.
Your job: turn ANY user input (text, email, voice transcript, rough notes) into a
structured PRD that the Architect Agent can use to build a technical spec.

Rules:
- Be specific about features. Vague = bad. Concrete = good.
- Only include features that can be built with Next.js + Supabase.
- If user asks for something outside Next.js + Supabase, add it to out_of_scope.
- estimated_credits: simple=50, medium=150, complex=400
- skill_hints: suggest relevant skill names from the skills library

Always output valid JSON matching the PRDSchema exactly. No markdown, no explanation.
Just the JSON object."""

class PMAgent(BaseAgent):
    name = "pm_agent"
    max_iterations = 1  # Single-shot with reflection

    def __init__(self):
        self.model = AnthropicModel("claude-sonnet-4-5")
        self.agent = Agent(
            model=self.model,
            result_type=PRDSchema,
            system_prompt=SYSTEM_PROMPT,
        )
        self.skill_loader = SkillLoader()

    async def observe(self, state: ForgeState) -> dict:
        # Load all skill metadata (L1 — ~100 tokens per skill)
        skills_context = self.skill_loader.load_all_metadata()
        return {
            "user_input": state.user_input,
            "input_type": state.input_type,
            "available_skills": [s.name for s in skills_context],
        }

    async def think(self, observation: dict, state: ForgeState) -> dict:
        prompt = f"""User request: {observation['user_input']}

Available skills (suggest relevant ones in skill_hints):
{chr(10).join(f'- {s}' for s in observation['available_skills'])}

Generate a complete PRD for this project."""
        return {"action": "generate_prd", "prompt": prompt}

    async def act(self, action: dict, state: ForgeState) -> dict:
        result = await self.agent.run(action["prompt"])
        return {"task_complete": True, "prd": result.data}

    async def on_complete(self, result: dict, state: ForgeState) -> ForgeState:
        state.prd = result["prd"]
        print(f"✓ PM Agent → PRD: {state.prd.project_name} [{state.prd.estimated_complexity}]")
        print(f"  Features: {len(state.prd.core_features)} | Credits: {state.prd.estimated_credits}")
        return state
```

### 2. forge/agents/architect.py (REPLACE STUB)
```python
from pydantic_ai import Agent
from pydantic_ai.models.anthropic import AnthropicModel
from forge.agents.base import BaseAgent
from forge.core.state import ForgeState, TechSpecSchema
from forge.skills.loader import SkillLoader

SYSTEM_PROMPT = """You are the Architect Agent for Forge.
Given a PRD, you design the complete technical specification for a Next.js 15 + Supabase app.

Your output must include:
- data_models: Supabase table schemas with all fields and relationships
- api_routes: every Next.js API route needed
- component_tree: nested component structure
- supabase_schema_sql: complete migration SQL (CREATE TABLE, RLS policies)
- skill_assignments: map each task to the best skill file
- agent_task_breakdown: split tasks between frontend_agent and backend_agent

IMPORTANT: Only use Next.js 15 (App Router) + Supabase. No other stacks.
Query the client's brand memory and constraints before designing.
Always output valid JSON matching TechSpecSchema exactly."""

SKILL_MAP_PROMPT = """Available skills (use these IDs in skill_assignments):
{skills}

Map each major task to the most relevant skill:
- auth tasks → supabase-auth or clerk-auth
- payment tasks → stripe-subscriptions or stripe-one-time
- dashboard UI → dashboard-layout
- data tables → data-table-crud
- marketing page → landing-page
- API routes → rest-crud
- webhooks → webhook-handler
- deployment → vercel-nextjs
- testing → playwright-e2e"""

class ArchitectAgent(BaseAgent):
    name = "architect"
    max_iterations = 1

    def __init__(self):
        self.model = AnthropicModel("claude-opus-4-5")
        self.agent = Agent(
            model=self.model,
            result_type=TechSpecSchema,
            system_prompt=SYSTEM_PROMPT,
        )
        self.skill_loader = SkillLoader()

    async def observe(self, state: ForgeState) -> dict:
        skills = self.skill_loader.load_all_metadata()
        return {
            "prd": state.prd.model_dump(),
            "skills": {s.id: s.description for s in skills},
        }

    async def think(self, observation: dict, state: ForgeState) -> dict:
        skills_str = "\n".join(
            f"- {sid}: {desc}"
            for sid, desc in observation["skills"].items()
        )
        prompt = f"""PRD:
{observation['prd']}

{SKILL_MAP_PROMPT.format(skills=skills_str)}

Design the complete technical specification."""
        return {"action": "generate_spec", "prompt": prompt}

    async def act(self, action: dict, state: ForgeState) -> dict:
        result = await self.agent.run(action["prompt"])
        return {"task_complete": True, "tech_spec": result.data}

    async def on_complete(self, result: dict, state: ForgeState) -> ForgeState:
        state.tech_spec = result["tech_spec"]
        spec = state.tech_spec
        print(f"✓ Architect → TechSpec: {len(spec.api_routes)} routes, {len(spec.data_models)} models")
        print(f"  Skills assigned: {spec.skill_assignments}")
        return state
```

### 3. forge/skills/loader.py (NEW FILE)
```python
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
import re

SKILLS_DIR = Path(__file__).parent.parent.parent / "forge-features" / "skills"

@dataclass
class SkillMetadata:
    """Level 1 — always loaded (~100 tokens)"""
    id: str
    name: str
    description: str
    category: str
    stack_requirements: list[str]
    success_rate: float = 1.0

class SkillLoader:
    """Progressive disclosure skill loader.
    L1 metadata: always in context (100 tokens per skill)
    L2 instructions: loaded when Architect assigns skill to task
    L3 resources: loaded on demand when L2 references them
    """

    def load_all_metadata(self) -> list[SkillMetadata]:
        """Load L1 metadata for ALL skills. Call once at agent startup."""
        skills = []
        for skill_file in SKILLS_DIR.rglob("*.skill.md"):
            metadata = self._extract_metadata(skill_file)
            if metadata:
                skills.append(metadata)
        return skills

    def load_instructions(self, skill_id: str) -> str:
        """Load L2 — full SKILL.md content. Called when task is assigned."""
        for skill_file in SKILLS_DIR.rglob("*.skill.md"):
            if skill_file.stem.replace(".skill", "") == skill_id:
                return skill_file.read_text()
        raise FileNotFoundError(f"Skill not found: {skill_id}")

    def _extract_metadata(self, path: Path) -> Optional[SkillMetadata]:
        content = path.read_text()
        lines = content.strip().split("\n")
        if not lines:
            return None
        name_line = lines[0].replace("# SKILL:", "").strip()
        desc_line = next(
            (l for l in lines if l.startswith("## What This Skill Does")), ""
        )
        desc_idx = lines.index(desc_line) + 1 if desc_line in lines else -1
        description = lines[desc_idx].strip() if desc_idx > 0 else name_line

        # Extract category from second line (> v1.0 | Category: auth | ...)
        category = "general"
        for line in lines[:5]:
            if "Category:" in line:
                match = re.search(r"Category:\s*(\w+)", line)
                if match:
                    category = match.group(1)
                break

        return SkillMetadata(
            id=path.stem.replace(".skill", ""),
            name=name_line,
            description=description[:120],
            category=category,
            stack_requirements=["next.js", "supabase"],
        )
```

### 4. tests/test_stage2.py
```python
import asyncio
import pytest
import os
from forge.core.state import ForgeState, TokenBudget
from forge.agents.pm_agent import PMAgent
from forge.agents.architect import ArchitectAgent
from forge.skills.loader import SkillLoader
import uuid

async def test_skill_loader():
    """Test skills load correctly."""
    loader = SkillLoader()
    skills = loader.load_all_metadata()
    assert len(skills) >= 10, f"Expected 10+ skills, got {len(skills)}"
    print(f"\n✅ Skill loader: {len(skills)} skills loaded")
    for s in skills:
        print(f"   [{s.category}] {s.id}: {s.description[:60]}")

async def test_pm_agent():
    """Test PM Agent produces valid PRD."""
    state = ForgeState(
        project_id=str(uuid.uuid4()),
        user_id="test",
        session_id=str(uuid.uuid4()),
        user_input="Build a SaaS project management tool with auth, team workspaces, and Stripe billing",
        token_budget=TokenBudget(),
    )
    agent = PMAgent()
    result = await agent.run(state)
    assert result.prd is not None
    assert result.prd.project_name
    assert len(result.prd.core_features) > 0
    assert result.prd.estimated_credits > 0
    print(f"\n✅ PM Agent test PASSED")
    print(f"   Project: {result.prd.project_name}")
    print(f"   Complexity: {result.prd.estimated_complexity}")
    print(f"   Skill hints: {result.prd.skill_hints}")

async def test_architect_agent():
    """Test Architect Agent produces valid TechSpec with skill assignments."""
    state = ForgeState(
        project_id=str(uuid.uuid4()),
        user_id="test",
        session_id=str(uuid.uuid4()),
        user_input="Build a SaaS billing dashboard",
        token_budget=TokenBudget(),
    )
    pm = PMAgent()
    state = await pm.run(state)
    arch = ArchitectAgent()
    state = await arch.run(state)
    assert state.tech_spec is not None
    assert len(state.tech_spec.api_routes) > 0
    assert state.tech_spec.supabase_schema_sql
    assert state.tech_spec.skill_assignments
    print(f"\n✅ Architect Agent test PASSED")
    print(f"   Routes: {len(state.tech_spec.api_routes)}")
    print(f"   Skills: {state.tech_spec.skill_assignments}")

if __name__ == "__main__":
    asyncio.run(test_skill_loader())
    asyncio.run(test_pm_agent())
    asyncio.run(test_architect_agent())
```

## ENVIRONMENT VARIABLES NEEDED FOR STAGE 2
```bash
ANTHROPIC_API_KEY=sk-ant-...     # Required — Claude Sonnet + Opus
LANGSMITH_API_KEY=...            # Optional but recommended for tracing
```

## VALIDATION — Stage 2 is DONE when:
- [ ] `python tests/test_stage2.py` passes all 3 tests
- [ ] PM Agent returns a valid PRDSchema with real features
- [ ] Architect maps tasks to correct skill IDs
- [ ] Skill loader finds all 11 skill files
- [ ] No Pydantic validation errors
- [ ] LangSmith shows trace (if configured)

## AFTER COMPLETING STAGE 2
1. FORGE_CODING_PROMPT.md → CURRENT STAGE → STATUS: DONE, move to Stage 3
2. forge-memory/NOW.md → update summary
3. forge-memory/PROJECT_INDEX.md → check off PM Agent + Architect Agent
4. `git commit -m "feat(stage-2): real PM + Architect agents with Claude + skill mapping"`

*Stage 2 — March 2026*
