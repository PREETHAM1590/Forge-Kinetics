from __future__ import annotations

from fastapi import Header, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class AuthContextMiddleware(BaseHTTPMiddleware):
	async def dispatch(self, request: Request, call_next):
		request.state.user_id = request.headers.get("x-user-id")
		return await call_next(request)


async def get_current_user_id(x_user_id: str | None = Header(default=None)) -> str:
	if not x_user_id:
		raise HTTPException(status_code=401, detail="Missing x-user-id header")
	return x_user_id

