
from typing import List

import logging

from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile, Form

from app.flow import Flow

from app.deps import get_flow


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/upload")
def create_upload_file(
        background_tasks: BackgroundTasks,
        files: List[UploadFile] = File(...),    
        append: bool = Form(None),
        extras: str = Form(None),
        flow: Flow = Depends(get_flow)):
    print("Extras", extras)
    background_tasks.add_task(flow.start_data_ingest, files, append, extras)
    return {"message": "Started data processing"}

@router.get("/count")
def get_dataset_length(flow: Flow = Depends(get_flow)):
    return flow.loader.count()


@router.get("/")
def get_dataset_length(
    page: int = 0,
    count: int = 10,
    flow: Flow = Depends(get_flow)):
    return flow.loader.load_data(page, count)