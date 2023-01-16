import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.api.v1 import api_router
from app.settings import settings, initialize_folder

from app.flow import Flow
import app.deps

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

initialize_folder('')
initialize_folder('listeners')

app.include_router(api_router, prefix=settings.API_V1_STR)
