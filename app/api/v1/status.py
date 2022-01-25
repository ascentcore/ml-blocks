

import logging

from fastapi import APIRouter, Depends

from app.deps import get_flow
from app.flow import Flow
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
def get_status(
    flow: Flow = Depends(get_flow)
    ):
    return flow.runtime.name

