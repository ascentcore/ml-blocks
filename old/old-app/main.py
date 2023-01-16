import logging
import sqlite3 as sql

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from starlette.middleware.cors import CORSMiddleware

from old.cached_version.flow import statics_folder
from old.cached_version.deps import get_registry

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

app.mount("/api/v1/download",
          StaticFiles(directory=statics_folder), name="generated")


@app.on_event('startup')
async def startup():
    conn = sql.connect('data/session.db')
    cur = conn.cursor()
    cur.execute("DELETE from graph")
    cur.execute("DELETE from block")
    cur.execute("DELETE from report")
    conn.commit()
    conn.close()

    get_registry()


@app.on_event("shutdown")
async def shutdown():
    logger.info('Shutting down... unregistering')
    get_registry().unsubscribe()
