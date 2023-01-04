import logging
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile, Form

from app.flow import Flow
from app.deps import get_flow

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/count")
def count(
    flow: Flow = Depends(get_flow)
):
    return flow.block.storage.count()


@router.get("/")
def get_dataset_length(
    page: int = 0,
    count: int = 10,
    format: str = None,
    flow: Flow = Depends(get_flow)
):
    return flow.query(page, count)


# @router.get("/formats")
# def get_formats(
#     flow: Flow = Depends(get_flow)
# ):
#     return flow.loader.formats()


# @router.put("/update_data")
# def update_data(
#     background_tasks: BackgroundTasks,
#     flow: Flow = Depends(get_flow)
# ):
#     background_tasks.add_task(
#         flow.update_data)
#     return {"message": "Started data processing"}
