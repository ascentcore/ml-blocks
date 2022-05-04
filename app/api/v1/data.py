import logging
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile, Form

from app.deps import get_flow, get_orm_db
from app.flow import Flow


logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/upload_files")
def create_upload_file(
    background_tasks: BackgroundTasks,
    files: List[UploadFile] = File(...),
    append: bool = Form(None),
    flow: Flow = Depends(get_flow)
):

    background_tasks.add_task(
        flow.load_data_files, files, append)
    return {"message": "Started data processing"}


@router.get("/count")
def count(
    flow: Flow = Depends(get_flow)
):
    return flow.loader.count()


@router.get("/")
def get_dataset_length(
    page: int = 0,
    count: int = 10,
    format: str = None,
    flow: Flow = Depends(get_flow)
):
    return flow.loader.query(page, count, format)
