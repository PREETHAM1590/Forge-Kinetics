from __future__ import annotations

from typing import Any

from fastapi import APIRouter

from forge.hitl.payload import HITLReviewPayload

router = APIRouter()
HITL_EVENTS: dict[str, dict[str, Any]] = {}


@router.post("/{project_id}/payload")
async def upsert_hitl_payload(project_id: str, payload: HITLReviewPayload) -> dict[str, Any]:
	data = payload.model_dump()
	HITL_EVENTS[project_id] = {"project_id": project_id, "payload": data, "decision": "pending"}
	return HITL_EVENTS[project_id]


@router.post("/{project_id}/approve")
async def approve_hitl(project_id: str, payload: dict[str, Any]) -> dict[str, Any]:
	state = HITL_EVENTS.setdefault(project_id, {"project_id": project_id, "payload": {}, "decision": "pending"})
	state["decision"] = "approved"
	state["approver_id"] = payload.get("approver_id", "unknown")
	return state


@router.post("/{project_id}/reject")
async def reject_hitl(project_id: str, payload: dict[str, Any]) -> dict[str, Any]:
	state = HITL_EVENTS.setdefault(project_id, {"project_id": project_id, "payload": {}, "decision": "pending"})
	state["decision"] = "rejected"
	state["reason"] = payload.get("reason", "not_provided")
	return state

