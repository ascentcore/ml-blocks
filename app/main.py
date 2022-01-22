import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from starlette.middleware.cors import CORSMiddleware

from .flow import statics_folder

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

# @app.get("/api/test")
# async def root():
#     return {"message": "Hello World"}

app.include_router(api_router, prefix=settings.API_V1_STR)

app.mount("/", StaticFiles(directory="/app/ui/", html=True), name="static")
app.mount("/api/v1/download", StaticFiles(directory=statics_folder), name="generated")

