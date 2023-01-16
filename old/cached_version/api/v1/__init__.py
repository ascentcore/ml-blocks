from fastapi import APIRouter

from . import data
from . import pipeline

api_router = APIRouter()

api_router.include_router(data.router, prefix="/data", tags=["data"])
api_router.include_router(pipeline.router, prefix="/pipeline", tags=["pipeline"])