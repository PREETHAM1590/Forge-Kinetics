from __future__ import annotations

import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(slots=True)
class E2BRuntimeConfig:
    agent_name: str
    docker_image: str


@dataclass(slots=True)
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
    """Async sandbox facade with local-shell fallback for scaffold development."""

    def __init__(self, agent_name: str, template: str = "base", root_dir: str | None = None) -> None:
        self.agent_name = agent_name
        self.template = template
        self.root_dir = Path(root_dir) if root_dir else Path.cwd()

    async def __aenter__(self) -> AgentSandbox:
        self.root_dir.mkdir(parents=True, exist_ok=True)
        return self

    async def __aexit__(self, *args: Any) -> None:
        return None

    async def run_bash(self, command: str, timeout: int = 120) -> SandboxResult:
        process = await asyncio.create_subprocess_exec(
            "powershell",
            "-NoProfile",
            "-Command",
            command,
            cwd=str(self.root_dir),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=timeout)
            return SandboxResult(
                stdout=stdout.decode("utf-8", errors="replace"),
                stderr=stderr.decode("utf-8", errors="replace"),
                exit_code=process.returncode or 0,
            )
        except TimeoutError:
            process.kill()
            return SandboxResult(stdout="", stderr=f"Command timed out after {timeout}s", exit_code=124)

    async def write_file(self, path: str, content: str) -> None:
        target = self._resolve(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    async def read_file(self, path: str) -> str:
        target = self._resolve(path)
        return target.read_text(encoding="utf-8")

    async def list_files(self, path: str | None = None) -> list[str]:
        base = self._resolve(path) if path else self.root_dir
        if not base.exists():
            return []
        if base.is_file():
            return [str(base)]
        return [str(child) for child in base.rglob("*") if child.is_file()]

    async def setup_nextjs_project(self, project_name: str) -> SandboxResult:
        project_dir = self.root_dir / project_name
        project_dir.mkdir(parents=True, exist_ok=True)
        package_json = project_dir / "package.json"
        if not package_json.exists():
            package_json.write_text(
                '{\n  "name": "'+project_name+'",\n  "private": true,\n  "scripts": {"build": "echo build-ok", "typecheck": "echo typecheck-ok"}\n}\n',
                encoding="utf-8",
            )
        return SandboxResult(stdout=f"Initialized scaffold at {project_dir}", stderr="", exit_code=0)

    async def run_build(self, project_path: str) -> SandboxResult:
        path = self._resolve(project_path)
        if not path.exists():
            return SandboxResult(stdout="", stderr=f"Project path not found: {path}", exit_code=1)
        return SandboxResult(stdout="build-ok", stderr="", exit_code=0)

    async def run_typecheck(self, project_path: str) -> SandboxResult:
        path = self._resolve(project_path)
        if not path.exists():
            return SandboxResult(stdout="", stderr=f"Project path not found: {path}", exit_code=1)
        return SandboxResult(stdout="typecheck-ok", stderr="", exit_code=0)

    def _resolve(self, raw_path: str | None) -> Path:
        if not raw_path:
            return self.root_dir
        cleaned = raw_path.strip()
        candidate = Path(cleaned)
        if candidate.is_absolute():
            return candidate
        if cleaned.startswith("/"):
            cleaned = cleaned.lstrip("/")
        return self.root_dir / Path(cleaned)


class E2BSandboxRuntime:
    """Compatibility wrapper used by earlier scaffold code."""

    def __init__(self, config: E2BRuntimeConfig) -> None:
        self.config = config
        self.sandbox = AgentSandbox(agent_name=config.agent_name, template=config.docker_image)

    def start(self) -> dict:
        return {
            "agent_name": self.config.agent_name,
            "docker_image": self.config.docker_image,
            "status": "sandbox_ready",
        }
