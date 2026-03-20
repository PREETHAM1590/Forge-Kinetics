from __future__ import annotations

from forge.sandbox.e2b_runtime import AgentSandbox, SandboxResult


async def init_project_repo(sandbox: AgentSandbox, project_path: str) -> SandboxResult:
    command = (
        f"Set-Location \"{project_path}\"; "
        "git init; "
        "git config user.email \"forge-agent@forge.dev\"; "
        "git config user.name \"Forge Agent\"; "
        "git add -A; "
        "git commit -m \"init: project scaffold\""
    )
    return await sandbox.run_bash(command)


async def commit_agent_work(sandbox: AgentSandbox, agent_name: str, project_path: str) -> SandboxResult:
    command = (
        f"Set-Location \"{project_path}\"; "
        "git add -A; "
        f"git commit -m \"feat({agent_name}): completed build\""
    )
    return await sandbox.run_bash(command)


async def get_diff_summary(sandbox: AgentSandbox, project_path: str) -> str:
    command = (
        f"Set-Location \"{project_path}\"; "
        "git log --oneline -n 10; "
        "Write-Output '---'; "
        "git diff HEAD~1 --stat"
    )
    result = await sandbox.run_bash(command)
    return result.stdout.strip()
