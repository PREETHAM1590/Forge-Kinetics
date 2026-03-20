from __future__ import annotations

from typing import Any
from uuid import uuid4

from fastapi import APIRouter, HTTPException

router = APIRouter()
PROJECTS: dict[str, dict[str, Any]] = {}


@router.get("")
async def list_projects() -> dict[str, list[dict[str, Any]]]:
	return {"items": list(PROJECTS.values())}


@router.post("")
async def create_project(payload: dict[str, Any]) -> dict[str, Any]:
	project_id = payload.get("project_id") or str(uuid4())
	project = {"project_id": project_id, "name": payload.get("name", "Untitled"), "status": "created"}
	PROJECTS[project_id] = project
	return project


@router.get("/{project_id}")
async def get_project(project_id: str) -> dict[str, Any]:
	project = PROJECTS.get(project_id)
	if not project:
		raise HTTPException(status_code=404, detail="project_not_found")
	return project

