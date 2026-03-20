from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class MaintenanceAgent:
    async def run_nightly_scan(self, project_id: str, deploy_url: str) -> dict:
        return {
            "project_id": project_id,
            "deploy_url": deploy_url,
            "has_issues": False,
            "status": "healthy",
        }
