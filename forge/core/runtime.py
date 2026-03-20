from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AgentRuntime:
    """OpenHands-style runtime placeholder for per-agent observe-think-act loop."""

    agent_name: str
    docker_image: str
    max_iterations: int = 20

    def run_iteration_loop(self) -> dict:
        return {
            "agent_name": self.agent_name,
            "docker_image": self.docker_image,
            "max_iterations": self.max_iterations,
            "status": "not_implemented",
        }
