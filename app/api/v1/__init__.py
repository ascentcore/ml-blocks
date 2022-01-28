from fastapi import APIRouter
from . import data, settings, status, statics, model

api_router = APIRouter()

# if settings.ENV_DEVELOPMENT:
api_router.include_router(data.router, prefix="/data", tags=["data"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(status.router, prefix="/status", tags=["status"])
api_router.include_router(statics.router, prefix="/statics", tags=["statics"])
api_router.include_router(model.router, prefix="/model", tags=["model"])
