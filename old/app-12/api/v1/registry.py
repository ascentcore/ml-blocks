import logging

from fastapi import APIRouter,  Depends, Request
from old.cached_version.deps import get_flow
from old.cached_version.flow import Flow

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/subscribe")
async def train(
    hostname: str,
    request: Request,
    flow: Flow = Depends(get_flow),
):
    logger.info(f'Called subscribe')
    data = await request.json()
    flow.registry.update_registry(hostname, data)


@router.delete("/subscribe")
async def train(
    hostname: str,
    flow: Flow = Depends(get_flow),
):
    logger.info(f'Called subscribe')
    flow.registry.delete(hostname)


@router.put("/update")
async def train(
    hostname: str,
    request: Request,
    flow: Flow = Depends(get_flow),
):
    logger.info(f'Updating registry for hostname: {hostname}')
    data = await request.json()
    flow.registry.update_registry(hostname, {}, data)


@router.get("/graph")
async def graph(flow: Flow = Depends(get_flow)):
    logger.info('Loading graph...')
    return flow.registry.get_graph()
