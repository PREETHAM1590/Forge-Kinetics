from __future__ import annotations

from typing import Any

from forge.scheduler.tasks import SCHEDULED_TASKS


async def run_scheduled_tasks() -> list[dict[str, Any]]:
	results: list[dict[str, Any]] = []
	for task in SCHEDULED_TASKS:
		results.append({"task": task["name"], "status": "queued", "agent": task["agent"]})
	return results

