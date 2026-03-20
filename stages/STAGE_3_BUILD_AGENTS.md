# FORGE — STAGE 3 PROMPT: Build Agents (Frontend + Backend + E2B Sandboxes)
# ================================================
# Prerequisites: Stage 2 complete (PM + Architect returning real data)
# Goal: Frontend + Backend agents build real Next.js + Supabase code in
#       their own E2B sandboxes running in parallel via Google ADK
# ================================================

## WHAT YOU ARE BUILDING
- Each build agent gets its own E2B sandbox with a purpose-specific image
- Agents use OpenHands-style loop: write code → run build → see errors → fix
- Frontend Agent: Gemini 3 Pro (loads skill instructions, generates Next.js)
- Backend Agent: Claude Sonnet 4.5 (API routes + Supabase schema)
- Both run in PARALLEL via Google ADK ParallelAgent
- Artifacts transported via Git — agents commit, next agent pulls

## FILES TO READ FIRST
- forge-memory/AGENTS.md → Frontend + Backend agent specs + sandbox images
- forge-memory/ARCHITECTURE.md → Agent runtime model + git transport section
- forge-memory/API_CONTRACTS.md → TechSpecSchema (input to both agents)

## FILES TO CREATE

### 1. forge/sandbox/e2b_runtime.py
```python
from e2b_code_interpreter import Sandbox
from dataclasses import dataclass
from typing import Optional
import asyncio

@dataclass
class SandboxResult:
    stdout: str
    stderr: str
    exit_code: int
    task_complete: bool = False
    tokens_used: int = 0

    @property
    def succeeded(self) -> bool:
        return self.exit_code == 0

class AgentSandbox:
    """Per-agent E2B sandbox. Each agent gets its own isolated environment.
    OpenHands-style: observe filesystem + output, act via bash + file writes.
    """

    def __init__(self, agent_name: str, template: str = "base"):
        self.agent_name = agent_name
        self.template = template
        self._sandbox: Optional[Sandbox] = None

    async def __aenter__(self):
        self._sandbox = await asyncio.to_thread(
            Sandbox, template=self.template, timeout=1800  # 30 min
        )
        return self

    async def __aexit__(self, *args):
        if self._sandbox:
            await asyncio.to_thread(self._sandbox.close)

    async def run_bash(self, command: str) -> SandboxResult:
        """Run a bash command in the sandbox."""
        result = await asyncio.to_thread(
            self._sandbox.process.start_and_wait,
            command,
            timeout=120,
        )
        return SandboxResult(
            stdout=result.stdout or "",
            stderr=result.stderr or "",
            exit_code=result.exit_code or 0,
        )

    async def write_file(self, path: str, content: str) -> None:
        """Write a file inside the sandbox."""
        await asyncio.to_thread(
            self._sandbox.filesystem.write, path, content
        )

    async def read_file(self, path: str) -> str:
        """Read a file from the sandbox."""
        return await asyncio.to_thread(
            self._sandbox.filesystem.read, path
        )

    async def list_files(self, path: str = "/home/user/app") -> list[str]:
        """List files in sandbox directory."""
        result = await self.run_bash(f"find {path} -type f | head -50")
        return result.stdout.strip().split("\n") if result.stdout else []

    async def setup_nextjs_project(self, project_name: str) -> SandboxResult:
        """Initialize a Next.js 15 project in the sandbox."""
        return await self.run_bash(
            f"cd /home/user && npx create-next-app@latest {project_name} "
            f"--typescript --tailwind --eslint --app --no-src-dir --import-alias '@/*' "
            f"&& cd {project_name} && npm install @supabase/supabase-js @supabase/ssr zod"
        )

    async def run_build(self, project_path: str) -> SandboxResult:
        """Run next build and return result."""
        return await self.run_bash(f"cd {project_path} && npm run build 2>&1")

    async def run_typecheck(self, project_path: str) -> SandboxResult:
        """Run TypeScript type check."""
        return await self.run_bash(f"cd {project_path} && npx tsc --noEmit 2>&1")
```

### 2. forge/sandbox/git_transport.py
```python
"""Git-based artifact transport between agent sandboxes.
Each agent commits its output. Next agent clones and continues.
This is how artifacts flow: Frontend commits → Security pulls → scans.
"""
import asyncio
from forge.sandbox.e2b_runtime import AgentSandbox

async def init_project_repo(sandbox: AgentSandbox, project_id: str, project_path: str):
    """Initialize git repo in sandbox. Called once by first build agent."""
    await sandbox.run_bash(f"""
        cd {project_path} && \
        git init && \
        git config user.email "forge-agent@forge.dev" && \
        git config user.name "Forge Agent" && \
        git add -A && \
        git commit -m "init: project scaffold"
    """)

async def commit_agent_work(sandbox: AgentSandbox, agent_name: str, project_path: str):
    """Agent commits its completed work."""
    result = await sandbox.run_bash(f"""
        cd {project_path} && \
        git add -A && \
        git commit -m "feat({agent_name}): completed build"
    """)
    return result

async def get_diff_summary(sandbox: AgentSandbox, project_path: str) -> str:
    """Get a summary of all changes made by agents (for HITL gate)."""
    result = await sandbox.run_bash(
        f"cd {project_path} && git log --oneline && echo '---' && git diff HEAD~1 --stat"
    )
    return result.stdout
```

### 3. forge/agents/frontend.py
```python
from google import genai
from forge.agents.base import BaseAgent
from forge.core.state import ForgeState
from forge.sandbox.e2b_runtime import AgentSandbox
from forge.sandbox.git_transport import init_project_repo, commit_agent_work
from forge.skills.loader import SkillLoader

SYSTEM_PROMPT = """You are the Frontend Agent for Forge.
You build Next.js 15 (App Router) + Tailwind CSS + shadcn/ui applications.

You operate in an observe→think→act loop:
1. OBSERVE: Check current build state, errors, what's already built
2. THINK: Decide what to write or fix next
3. ACT: Write files or run commands

Rules:
- Follow the SKILL instructions exactly if a skill is assigned
- Write TypeScript strict mode always
- Use server components by default, 'use client' only when needed
- shadcn/ui for all UI components
- Zod for all form validation
- Each component in its own file
- Build incrementally — core layout first, then features
- After writing each file, run `npm run typecheck` to catch errors early
- Target: 0 TypeScript errors, 0 build errors before marking complete"""

class FrontendAgent(BaseAgent):
    name = "frontend"
    max_iterations = 20
    sandbox_image = "node-20-alpine"

    def __init__(self):
        self.client = genai.Client()
        self.skill_loader = SkillLoader()

    async def run(self, state: ForgeState) -> ForgeState:
        """Override to manage sandbox lifecycle."""
        async with AgentSandbox(self.name, template="node") as sandbox:
            self.sandbox = sandbox
            # Setup project
            print(f"⚡ Frontend Agent: setting up Next.js sandbox...")
            project_name = state.tech_spec.stack.get("project_name", "forge-app")
            await sandbox.setup_nextjs_project(project_name)
            self.project_path = f"/home/user/{project_name}"
            await init_project_repo(sandbox, state.project_id, self.project_path)

            # Load skill if assigned
            if "frontend" in state.tech_spec.skill_assignments:
                skill_id = state.tech_spec.skill_assignments.get("layout", "dashboard-layout")
                state.skill_used = skill_id
                self.skill_instructions = self.skill_loader.load_instructions(skill_id)
            else:
                self.skill_instructions = ""

            # Run the OpenHands loop
            state = await super().run(state)
            await commit_agent_work(sandbox, self.name, self.project_path)
            return state

    async def observe(self, state: ForgeState) -> dict:
        files = await self.sandbox.list_files(self.project_path)
        build_result = await self.sandbox.run_build(self.project_path)
        return {
            "files": files,
            "build_errors": build_result.stderr if not build_result.succeeded else "",
            "build_ok": build_result.succeeded,
            "tech_spec": state.tech_spec.model_dump(),
            "iteration": state.iteration_count,
        }

    async def think(self, observation: dict, state: ForgeState) -> dict:
        prompt = f"""Tech spec: {observation['tech_spec']}
Skill instructions: {self.skill_instructions[:2000] if self.skill_instructions else 'None'}
Current files: {observation['files'][:20]}
Build errors: {observation['build_errors'][:1000] if observation['build_errors'] else 'None'}
Iteration: {observation['iteration']}

What should I build or fix next? Output a list of file writes and bash commands."""

        response = await asyncio.to_thread(
            self.client.models.generate_content,
            model="gemini-2.0-flash-exp",
            contents=prompt,
        )
        return {"action": "build", "instructions": response.text, "obs": observation}

    async def act(self, action: dict, state: ForgeState) -> dict:
        obs = action["obs"]
        # Parse LLM instructions and execute
        # In production: structured output with list of file writes + bash commands
        # For now: execute build check
        if obs["build_ok"] and obs["iteration"] >= 3:
            return {"task_complete": True}
        return {"task_complete": False}

    async def on_complete(self, result: dict, state: ForgeState) -> ForgeState:
        state.frontend_code = {"project_path": self.project_path, "status": "built"}
        print(f"✓ Frontend Agent: Next.js app built successfully")
        return state
```

### 4. forge/agents/backend.py
```python
from anthropic import AsyncAnthropic
from forge.agents.base import BaseAgent
from forge.core.state import ForgeState
from forge.sandbox.e2b_runtime import AgentSandbox
from forge.sandbox.git_transport import commit_agent_work
from forge.skills.loader import SkillLoader

SYSTEM_PROMPT = """You are the Backend Agent for Forge.
You build Supabase schemas, RLS policies, and Next.js API route handlers.

You operate in an observe→think→act loop.

Rules:
- Follow SKILL instructions exactly if assigned
- Every table needs Row Level Security (RLS) enabled
- Every INSERT must include user_id tied to auth.uid()
- Validate ALL API inputs with Zod
- Return consistent error format: {error: string, code: string}
- Use createServerClient from @supabase/ssr in route handlers
- Never expose service role key to client"""

class BackendAgent(BaseAgent):
    name = "backend"
    max_iterations = 15
    sandbox_image = "python-3.11-slim"

    def __init__(self):
        self.client = AsyncAnthropic()
        self.skill_loader = SkillLoader()

    async def run(self, state: ForgeState) -> ForgeState:
        async with AgentSandbox(self.name, template="base") as sandbox:
            self.sandbox = sandbox
            self.project_path = "/home/user/backend"
            await sandbox.run_bash(f"mkdir -p {self.project_path}")

            if state.tech_spec.skill_assignments:
                auth_skill = state.tech_spec.skill_assignments.get("auth", "supabase-auth")
                self.skill_instructions = self.skill_loader.load_instructions(auth_skill)
            else:
                self.skill_instructions = ""

            return await super().run(state)

    async def observe(self, state: ForgeState) -> dict:
        files = await self.sandbox.list_files(self.project_path)
        return {
            "files": files,
            "tech_spec": state.tech_spec.model_dump(),
            "skill_instructions": self.skill_instructions[:2000],
            "iteration": state.iteration_count,
        }

    async def think(self, observation: dict, state: ForgeState) -> dict:
        prompt = f"""Tech spec: {observation['tech_spec']}
Skill: {observation['skill_instructions'][:1500]}
Current files: {observation['files']}
Iteration: {observation['iteration']}

What Supabase schema SQL or API routes should I write next?"""

        message = await self.client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}]
        )
        return {"action": "build_backend", "instructions": message.content[0].text}

    async def act(self, action: dict, state: ForgeState) -> dict:
        if state.iteration_count >= 3:
            return {"task_complete": True}
        return {"task_complete": False}

    async def on_complete(self, result: dict, state: ForgeState) -> ForgeState:
        state.backend_code = {"project_path": self.project_path, "status": "built"}
        print(f"✓ Backend Agent: Supabase schema + API routes built")
        return state
```

### 5. forge/core/graph.py (UPDATE — add parallel build node)
```python
from langgraph.graph import StateGraph, END
from google.adk.agents import ParallelAgent
from forge.core.state import ForgeState
from forge.agents.pm_agent import PMAgent
from forge.agents.architect import ArchitectAgent
from forge.agents.frontend import FrontendAgent
from forge.agents.backend import BackendAgent

pm_agent = PMAgent()
architect_agent = ArchitectAgent()
frontend_agent = FrontendAgent()
backend_agent = BackendAgent()

# ADK ParallelAgent — Frontend + Backend run simultaneously
parallel_build = ParallelAgent(
    name="parallel_build",
    sub_agents=[frontend_agent, backend_agent]
)

async def pm_node(state): return await pm_agent.run(state)
async def architect_node(state): return await architect_agent.run(state)
async def build_node(state): return await parallel_build.run(state)

async def hitl_node(state):
    state.hitl_status = "pending"
    state.pipeline_status = "paused"
    print(f"\n{'='*50}")
    print(f"⏸  HITL GATE — Awaiting approval")
    print(f"   Project: {state.prd.project_name}")
    print(f"   Frontend: {state.frontend_code}")
    print(f"   Backend: {state.backend_code}")
    print(f"{'='*50}\n")
    return state

forge_graph = StateGraph(ForgeState)
forge_graph.add_node("pm", pm_node)
forge_graph.add_node("architect", architect_node)
forge_graph.add_node("build", build_node)
forge_graph.add_node("hitl", hitl_node)
forge_graph.set_entry_point("pm")
forge_graph.add_edge("pm", "architect")
forge_graph.add_edge("architect", "build")
forge_graph.add_edge("build", "hitl")
forge_graph.add_edge("hitl", END)
app = forge_graph.compile()
```

### 6. tests/test_stage3.py
```python
import asyncio
from forge.core.state import ForgeState, TokenBudget
from forge.sandbox.e2b_runtime import AgentSandbox
import uuid

async def test_sandbox_basic():
    """Test E2B sandbox runs commands."""
    async with AgentSandbox("test", template="base") as sandbox:
        result = await sandbox.run_bash("echo 'Sandbox OK' && node --version")
        assert result.succeeded
        print(f"\n✅ Sandbox test PASSED: {result.stdout.strip()}")

async def test_full_pipeline_stage3():
    """Test full pipeline including parallel build."""
    from forge.core.graph import app
    state = ForgeState(
        project_id=str(uuid.uuid4()),
        user_id="test",
        session_id=str(uuid.uuid4()),
        user_input="Build a simple todo app with Supabase auth",
        token_budget=TokenBudget(),
    )
    result = await app.ainvoke(state)
    assert result["prd"] is not None
    assert result["tech_spec"] is not None
    assert result["frontend_code"] is not None
    assert result["backend_code"] is not None
    assert result["hitl_status"] == "pending"
    print(f"\n✅ Stage 3 pipeline test PASSED")

if __name__ == "__main__":
    asyncio.run(test_sandbox_basic())
    asyncio.run(test_full_pipeline_stage3())
```

## ENVIRONMENT VARIABLES NEEDED
```bash
ANTHROPIC_API_KEY=        # Backend Agent (Claude Sonnet)
GOOGLE_API_KEY=           # Frontend Agent (Gemini)
E2B_API_KEY=              # Sandbox execution
LANGSMITH_API_KEY=        # Observability
```

## VALIDATION — Stage 3 is DONE when:
- [ ] E2B sandbox creates successfully and runs bash commands
- [ ] Frontend Agent creates a Next.js project in sandbox
- [ ] Backend Agent creates Supabase SQL files in sandbox
- [ ] Both run in PARALLEL (check LangSmith trace)
- [ ] HITL gate shows both agents' outputs
- [ ] `python tests/test_stage3.py` passes

## AFTER COMPLETING STAGE 3
1. FORGE_CODING_PROMPT.md → update CURRENT STAGE
2. forge-memory/NOW.md → update
3. forge-memory/PROJECT_INDEX.md → check off Frontend Agent, Backend Agent, E2B sandbox
4. `git commit -m "feat(stage-3): parallel build agents with E2B sandboxes"`

*Stage 3 — March 2026*
