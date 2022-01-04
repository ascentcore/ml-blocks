import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from starlette.middleware.cors import CORSMiddleware

from .api.v1.api import api_router
from .core.config import settings

from .store import cleanup

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


app.mount("/ui", StaticFiles(directory="/app/ml-blocks-ui/dist", html=True), name="static")
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.on_event("startup")
def start_event():
    cleanup()