import logging

from fastapi import APIRouter, Depends
from app.settings import settings
from app.deps import get_flow
from app.flow import Flow


logger = logging.getLogger(__name__)
router = APIRouter()


@router.put("/trigger")
def get_dataset_length(
    stage: str,
    flow: Flow = Depends(get_flow)
):
    return flow.trigger(stage)


@router.get("/stage")
def get_dataset_length():
    with open(f'{settings.MOUNT_FOLDER}/internal/stage', 'r') as infile:
        return infile.read()
