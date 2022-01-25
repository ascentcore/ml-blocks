import logging
import asyncio

from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles

from starlette.middleware.cors import CORSMiddleware

from app.flow import Flow, statics_folder
from app.deps import get_flow

from .broker import connect_to_queue

from .api.v1 import api_router
from .config import settings

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

app.mount("/", StaticFiles(directory="/app/ui/", html=True), name="static")
app.mount("/api/v1/download",
          StaticFiles(directory=statics_folder), name="generated")


task = None

@app.on_event('startup')
async def startup(flow: Flow = Depends(get_flow)):
    global task
    logger.info('ML-Blocks startup complete...')
    loop = asyncio.get_event_loop()
    task = loop.create_task(connect_to_queue(loop, flow))

@app.on_event('shutdown')
async def shutdown():
    logger.info('Killing task...')
    task.cancel()