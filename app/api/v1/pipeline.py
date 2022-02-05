import logging
from fastapi import APIRouter, Depends, Request, BackgroundTasks
from app.flow import Flow

from app.registry import Registry
from app.db import models

from app.deps import get_flow, get_registry, get_orm_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.put("/register")
def register(
    request: Request,
    db=Depends(get_orm_db),
    registry: Registry = Depends(get_registry)
):
    registry.register(db, request.client.host)


@router.get("/dependencies")
def register(db=Depends(get_orm_db)):
    return db.query(models.Dependency).all()


@router.get("/status")
def status(registry: Registry = Depends(get_registry)):
    return {
        "connected": registry.connected,
        "dependency_url": registry.get_dependency_url()
    }


@router.get("/loader")
def get_loader(flow: Flow = Depends(get_flow)):
    return type(flow.loader).__name__


@router.get("/content_types")
def get_loader(flow: Flow = Depends(get_flow)):
    return flow.loader.export_content_types()


@router.post("/rebuild")
def rebuild(
        background_tasks: BackgroundTasks,
        flow: Flow = Depends(get_flow),
        registry: Registry = Depends(get_registry),
        db=Depends(get_orm_db)):

    background_tasks.add_task(registry.rebuild_from_upstream, flow, db)

    if registry.connected:
        logger.info('Rebuilding...')
        pass
    else:
        logger.info('Unable to rebuild. Not connected to dependency')
