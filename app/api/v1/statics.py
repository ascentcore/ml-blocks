

import logging
import os

from fastapi import APIRouter, BackgroundTasks, Depends

from app.deps import get_flow, get_orm_db
from app.flow import Flow
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/generate_statics")
def generate_statics(
        background_tasks: BackgroundTasks,
        flow: Flow = Depends(get_flow),
         db=Depends(get_orm_db)):

    background_tasks.add_task(flow.generate_statics, db)
    return {"message": "Started generation of static resources"}


@router.get("/")
def get_dataset_length(flow: Flow = Depends(get_flow)):
    return flow.list_statics()