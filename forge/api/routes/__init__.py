from fastapi import APIRouter

from forge.api.routes.credits import router as credits_router
from forge.api.routes.hitl import router as hitl_router
from forge.api.routes.pipeline import router as pipeline_router
from forge.api.routes.projects import router as projects_router
from forge.api.routes.webhooks import router as webhooks_router

api_router = APIRouter()
api_router.include_router(projects_router, prefix="/projects", tags=["projects"])
api_router.include_router(pipeline_router, prefix="/pipeline", tags=["pipeline"])
api_router.include_router(hitl_router, prefix="/hitl", tags=["hitl"])
api_router.include_router(credits_router, prefix="/credits", tags=["credits"])
api_router.include_router(webhooks_router, prefix="/webhooks", tags=["webhooks"])

__all__ = ["api_router"]

