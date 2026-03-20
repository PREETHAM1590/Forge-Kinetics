from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()
CREDIT_BALANCE: dict[str, int] = {}


@router.get("/{user_id}")
async def get_credits(user_id: str) -> dict[str, int | str]:
	return {"user_id": user_id, "credits": CREDIT_BALANCE.get(user_id, 0)}


@router.post("/{user_id}/debit")
async def debit_credits(user_id: str, payload: dict[str, int]) -> dict[str, int | str]:
	amount = max(int(payload.get("amount", 0)), 0)
	current = CREDIT_BALANCE.get(user_id, 0)
	CREDIT_BALANCE[user_id] = max(current - amount, 0)
	return {"user_id": user_id, "credits": CREDIT_BALANCE[user_id]}

