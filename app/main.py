import logging

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from starlette.middleware.cors import CORSMiddleware


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

@app.get("/api/test")
async def root():
    return {"message": "Hello World"}

app.mount("/", StaticFiles(directory="/app/ui/", html=True), name="static")
# app.mount("/generated/download", StaticFiles(directory="/app/generated", html=True), name="generated")

