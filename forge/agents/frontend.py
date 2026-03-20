from __future__ import annotations

import asyncio
from dataclasses import dataclass

from forge.core.state import ForgeState
from forge.sandbox.e2b_runtime import AgentSandbox
from forge.sandbox.git_transport import commit_agent_work, init_project_repo


@dataclass(slots=True)
class FrontendAgent:
    """Stage 3 frontend scaffold agent with sandbox lifecycle hooks."""

    name: str = "frontend"
    sandbox_template: str = "node"

    async def run_async(self, state: ForgeState) -> ForgeState:
        project_name = state.tech_spec.stack.get("project_name", "forge-app") if state.tech_spec else "forge-app"
        async with AgentSandbox(self.name, template=self.sandbox_template) as sandbox:
            setup = await sandbox.setup_nextjs_project(project_name)
            project_path = str((sandbox.root_dir / project_name).resolve())
            await init_project_repo(sandbox, project_path)
            await sandbox.write_file(
                f"{project_path}/frontend_status.txt",
                "frontend scaffold build completed",
            )
            typecheck = await sandbox.run_typecheck(project_path)
            build = await sandbox.run_build(project_path)
            await commit_agent_work(sandbox, self.name, project_path)

        state.frontend_code = {
            "status": "built" if (setup.succeeded and build.succeeded and typecheck.succeeded) else "needs_attention",
            "project_path": project_path,
            "setup_stdout": setup.stdout.strip(),
            "build_stdout": build.stdout.strip(),
            "typecheck_stdout": typecheck.stdout.strip(),
        }
        state.current_agent = "frontend_agent"
        return state

    def run(self, state: ForgeState) -> ForgeState:
        return asyncio.run(self.run_async(state))
