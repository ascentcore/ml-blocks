
from typing import List

import logging

from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile, Form

from app.flow import Flow

from app.deps import get_flow, get_orm_db, get_registry
from app.registry import Registry


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


def ingest_data_and_notify_downstream(flow, registry, files, append, extras, db):
    logger.info('Started data processing ...')
    flow.start_data_ingest(db, files, append, extras)
    logger.info('Notifying downstream dependencies ....')
    registry.notify_downstream(db)
    logger.info('Ingestion complete')


@router.post("/upload")
def create_upload_file(
        background_tasks: BackgroundTasks,
        files: List[UploadFile] = File(...),
        append: bool = Form(None),
        extras: str = Form(None),
        flow: Flow = Depends(get_flow),
        registry: Registry = Depends(get_registry),
        db=Depends(get_orm_db)):

    background_tasks.add_task(
        ingest_data_and_notify_downstream, flow, registry, files, append, extras, db)
    return {"message": "Started data processing"}


@router.post("/append")
def append_data(
    background_tasks: BackgroundTasks,
    append: bool = Form(None),
    extras: str = Form(None),
    flow: Flow = Depends(get_flow),
    registry: Registry = Depends(get_registry),
    db=Depends(get_orm_db)):

    background_tasks.add_task(
        ingest_data_and_notify_downstream, flow, registry, files, append, extras, db)
    return {"message": "Started data processing"}


@router.get("/count")
def get_dataset_length(flow: Flow = Depends(get_flow)):
    return flow.loader.count()


@router.put("/process_data")
def process_data(
        background_tasks: BackgroundTasks,
        flow: Flow = Depends(get_flow)):

    # background_tasks.add_task(flow.process_data)
    flow.process_data()


@router.get("/")
def get_dataset_length(
        page: int = 0,
        count: int = 10,
        format: str = '',
        flow: Flow = Depends(get_flow)):
    logger.info('Loading data...')

    return flow.loader.load_data(page, count, format)
