import logging
from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends, File, Request, Form

from app.flow import Flow
from app.deps import get_flow

logger = logging.getLogger(__name__)
router = APIRouter()


@router.put("/register")
async def register(
    hostname: str,
    flow: Flow = Depends(get_flow)
):
    logger.info(f'Called subscribe')
    flow.register(hostname)
    pass
