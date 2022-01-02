import logging

from typing import Generator, Optional
from fastapi import FastAPI, File, UploadFile, Form, Request

from .loaders.loader_factory import get_loader

from .runtime import runtime

from .api.v1.api import api_router
from .core.config import settings

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

loader = get_loader(runtime.loader, {})

app = FastAPI()


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...), append: bool = Form(None)):    
    logger.info('File uploaded. Processing...')
    loader.load_file(file.file)
    runtime.process_dataset(loader.data)
    loader.store(append)

app.include_router(api_router, prefix=settings.API_V1_STR)