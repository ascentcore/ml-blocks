import logging
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, File, UploadFile, Form

from app.deps import get_flow
from app.flow import Flow


logger = logging.getLogger(__name__)
router = APIRouter()


@router.put("/train")
def train(
    background_tasks: BackgroundTasks,
    flow: Flow = Depends(get_flow)
):
    flow.stage = 'train'
    background_tasks.add_task(flow.next, False)
    return {"message": "Started model training"}
