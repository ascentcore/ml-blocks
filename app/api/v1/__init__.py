from fastapi import APIRouter

from . import data

api_router = APIRouter()

# if settings.ENV_DEVELOPMENT:
api_router.include_router(data.router, prefix="/data", tags=["data"])
