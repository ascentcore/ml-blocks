

import logging
import os

from fastapi import APIRouter, BackgroundTasks, Depends

from app.deps import get_flow
from app.flow import Flow
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/generate_statics")
def generate_statics(
        background_tasks: BackgroundTasks,
        flow: Flow = Depends(get_flow)):

    background_tasks.add_task(flow.generate_statics)
    return {"message": "Started generation of static resources"}


@router.get("/")
def get_dataset_length(flow: Flow = Depends(get_flow)):
    test = flow.list_statics()
    return test