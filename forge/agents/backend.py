from __future__ import annotations

import asyncio
from dataclasses import dataclass

from forge.core.state import ForgeState
from forge.sandbox.e2b_runtime import AgentSandbox
from forge.sandbox.git_transport import commit_agent_work, init_project_repo


@dataclass(slots=True)
class BackendAgent:
    """Stage 3 backend scaffold agent with sandbox lifecycle hooks."""

    name: str = "backend"
    sandbox_template: str = "python"

    async def run_async(self, state: ForgeState) -> ForgeState:
        async with AgentSandbox(self.name, template=self.sandbox_template) as sandbox:
            project_path = str((sandbox.root_dir / "forge-backend").resolve())
            await sandbox.run_bash(f"New-Item -ItemType Directory -Force -Path \"{project_path}\" | Out-Null")
            await init_project_repo(sandbox, project_path)

            schema_sql = state.tech_spec.supabase_schema_sql if state.tech_spec else "-- pending tech spec"
            api_routes = state.tech_spec.api_routes if state.tech_spec else []
            await sandbox.write_file(
                f"{project_path}/schema.sql",
                schema_sql,
            )
            await sandbox.write_file(
                f"{project_path}/api_routes.json",
                str(api_routes),
            )
            commit = await commit_agent_work(sandbox, self.name, project_path)

        state.backend_code = {
            "status": "built" if commit.succeeded else "needs_attention",
            "project_path": project_path,
            "api_routes_count": len(api_routes),
        }
        state.current_agent = "backend_agent"
        return state

    def run(self, state: ForgeState) -> ForgeState:
        return asyncio.run(self.run_async(state))
