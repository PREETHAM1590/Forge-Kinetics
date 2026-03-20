from __future__ import annotations

from typing import Any

from fastapi import APIRouter

router = APIRouter()
PIPELINE_STATE: dict[str, dict[str, Any]] = {}


@router.get("/{project_id}")
async def get_pipeline(project_id: str) -> dict[str, Any]:
	return PIPELINE_STATE.get(project_id, {"project_id": project_id, "status": "not_started", "events": []})


@router.post("/{project_id}/events")
async def append_pipeline_event(project_id: str, payload: dict[str, Any]) -> dict[str, Any]:
	state = PIPELINE_STATE.setdefault(project_id, {"project_id": project_id, "status": "running", "events": []})
	state["events"].append(payload)
	if "status" in payload:
		state["status"] = payload["status"]
	return state

