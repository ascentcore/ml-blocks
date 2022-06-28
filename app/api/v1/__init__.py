from fastapi import APIRouter

from . import data
from . import flow
from . import model
from . import statics

api_router = APIRouter()

# if settings.ENV_DEVELOPMENT:
api_router.include_router(data.router, prefix="/data", tags=["data"])
api_router.include_router(flow.router, prefix="/flow", tags=["flow"])
api_router.include_router(model.router, prefix="/model", tags=["model"])
api_router.include_router(statics.router, prefix="/statics", tags=["statics"])
