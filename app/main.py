import logging
import asyncio

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

from fastapi_utils.tasks import repeat_every

from starlette.middleware.cors import CORSMiddleware

from app.flow import Flow, statics_folder
from app.deps import get_flow, get_registry
from app.db.crud import set_status, cleanup
from app.constants import stages
from app.db import session

from .api.v1 import api_router
from .config import settings
from .registry import Registry

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

app.mount("/api/v1/download",
          StaticFiles(directory=statics_folder), name="generated")


initialized = False

@app.on_event('startup')
@repeat_every(seconds=60)
async def startup():
    db = session.SessionLocal()

    global initialized
    if not initialized:
        # cleanup(db)
        set_status(db, 'pending')
        logger.info('ML-Blocks startup complete...')
    
    
    registry = get_registry()
    registry.recreate_upstream_connections()

    db.close()

    initialized = True
