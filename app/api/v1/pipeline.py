from sqlalchemy import or_
import logging
import requests

from typing import Optional

from fastapi import APIRouter, Depends, Query, Request, BackgroundTasks, Response, Body
from app.flow import Flow
from app.config import settings
from app.registry import Registry
from app.db import models

from app.constants import DEPENDENCY_DATA_TYPE, DEPENDENCY_LOGIC_TYPE

from app.deps import get_flow, get_registry, get_orm_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.get('/hosts')
def hosts(db=Depends(get_orm_db)):
    return db.query(models.Block).all()


@router.put("/register")
def register(
    name: str,
    request: Request,
    db=Depends(get_orm_db),
    registry: Registry = Depends(get_registry)
):
    registry.register(db, request.client.host, name)


@router.delete("/register")
def unregister(
    request: Request,
    db=Depends(get_orm_db),
    registry: Registry = Depends(get_registry)
):
    registry.unregister(db, request.client.host)


@router.post("/reconfigure")
async def reconfigure(
        request: Request,
        db=Depends(get_orm_db)):
    json_data = await request.json()
    current = json_data['current']
    data = json_data['data'] if 'data' in json_data.keys() else None
    logic = json_data['logic'] if 'logic' in json_data.keys() else None

    db.query(models.Graph).filter_by(downstream=current).delete()

    if data:
        edge = models.Graph(upstream=data,
                            downstream=current,
                            edge_type=DEPENDENCY_DATA_TYPE)
        db.merge(edge)

    if logic:
        for item in logic:
            edge = models.Graph(upstream=item,
                                downstream=current,
                                edge_type=DEPENDENCY_LOGIC_TYPE)
            db.merge(edge)

    db.commit()


@router.put("/edge")
def edge(
    request: Request,
    edge_type: int,
    downstream: str,
    upstream: Optional[str] = Query(None),
    db=Depends(get_orm_db),
    registry: Registry = Depends(get_registry)
):
    registry.create_edge(db, upstream if upstream !=
                         None else request.client.host, downstream, edge_type)


@router.get("/graph")
def graph(upstream: str = None,
          downstream: str = None,
          edge_type: int = None,
          registry: Registry = Depends(get_registry),
          db=Depends(get_orm_db)):

    return registry.get_graph(db, upstream, downstream, edge_type)


@router.delete("/graph")
def graph(
    db=Depends(get_orm_db)
):
    registered_blocks = db.query(models.Block).all()

    to_remove = []
    for block in registered_blocks:
        try:
            request = requests.get(
                f'http://{block.host}/api/v1/status')
            print(request.status_code, block.host)
            if request.status_code != 200:
                to_remove.append(block.host)
        except:
            to_remove.append(block.host)
            pass

    db.query(models.Block).filter(models.Block.host.in_(to_remove)).delete()
    db.query(models.Graph).filter(
        or_(
            models.Graph.downstream.in_(to_remove),
            models.Graph.upstream.in_(to_remove))
    ).delete()

    db.commit()

    return to_remove


@ router.get("/status")
def status(registry: Registry = Depends(get_registry)):
    return {
        "connected": registry.connected,
        "dependency_url": registry.get_dependency_url()
    }


@ router.get("/loader")
def get_loader(flow: Flow = Depends(get_flow)):
    return type(flow.loader).__name__


@ router.get("/content_types")
def get_loader(flow: Flow = Depends(get_flow)):
    return flow.loader.export_content_types()


@ router.post("/rebuild")
def rebuild(
        background_tasks: BackgroundTasks,
        flow: Flow = Depends(get_flow),
        registry: Registry = Depends(get_registry),
        db=Depends(get_orm_db)):
    background_tasks.add_task(registry.rebuild_from_upstream, flow, db)
