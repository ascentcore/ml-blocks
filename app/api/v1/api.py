from fastapi import APIRouter

from app.core.config import settings
from .endpoints import info, data, model, pipe, generated

api_router = APIRouter()

if settings.ENV_DEVELOPMENT:
    api_router.include_router(info.router, prefix="/info", tags=["info"])
    api_router.include_router(data.router, prefix="/data", tags=["data"])
    api_router.include_router(model.router, prefix="/model", tags=["model"])
    api_router.include_router(pipe.router, prefix="/pipe", tags=["pipe"])
    api_router.include_router(generated.router, prefix="/generated", tags=["generated"])