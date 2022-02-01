import logging
from fastapi import APIRouter, Depends, Request

from app.flow import Flow
from app.deps import get_flow

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/")
def get_status(
    flow: Flow = Depends(get_flow)
):
    return flow.runtime.name
