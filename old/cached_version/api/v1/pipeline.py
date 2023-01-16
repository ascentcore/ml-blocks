import logging

from fastapi import APIRouter, Depends

from old.cached_version.flow import Flow
from old.cached_version.deps import get_flow

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
