from __future__ import annotations

from fastapi import FastAPI

from forge.api.middleware.auth import AuthContextMiddleware
from forge.api.middleware.rate_limit import RateLimitMiddleware
from forge.api.routes import api_router


def create_app() -> FastAPI:
	app = FastAPI(title="Forge API", version="1.0.0")
	app.add_middleware(RateLimitMiddleware)
	app.add_middleware(AuthContextMiddleware)
	app.include_router(api_router, prefix="/api")

	@app.get("/health")
	async def health() -> dict[str, str]:
		return {"status": "ok"}

	return app


app = create_app()

