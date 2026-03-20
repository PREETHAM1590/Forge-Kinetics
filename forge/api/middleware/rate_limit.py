from __future__ import annotations

import time
from collections import defaultdict

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
	def __init__(self, app, requests_per_minute: int = 120):
		super().__init__(app)
		self.requests_per_minute = requests_per_minute
		self._buckets: dict[str, list[float]] = defaultdict(list)

	async def dispatch(self, request: Request, call_next):
		now = time.time()
		key = request.client.host if request.client else "unknown"
		bucket = self._buckets[key]
		window_start = now - 60
		bucket[:] = [timestamp for timestamp in bucket if timestamp >= window_start]

		if len(bucket) >= self.requests_per_minute:
			return JSONResponse(status_code=429, content={"error": "rate_limited"})

		bucket.append(now)
		return await call_next(request)

