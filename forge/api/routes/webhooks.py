from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.post("/stripe")
async def stripe_webhook(payload: dict) -> dict[str, str]:
	event_type = str(payload.get("type", "unknown"))
	return {"status": "accepted", "event_type": event_type}

