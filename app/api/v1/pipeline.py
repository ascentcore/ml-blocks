import logging
import requests

from typing import Optional

from fastapi import APIRouter, Depends, Query, Request, BackgroundTasks, Response, Body
from app.flow import Flow
from app.config import settings
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
def graph(db=Depends(get_orm_db)):
    return db.query(models.Graph).all()


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
    # registry.rebuild_from_upstream(flow, db)

@router.get("/proxy")
def get_loader(ip: str, path: str):
    t_resp = requests.get(f'http://{ip}/{path}')
    response = Response(content=t_resp.content, status_code=t_resp.status_code, headers={
                        'content-type': 'application/json'})
    return response


@router.post("/proxy")
async def post_proxy(ip: str, path: str, request: Request):
    body = await request.json()
    t_resp = requests.post(f'http://{ip}/{path}', json = body)
    response = Response(content=t_resp.content, status_code=t_resp.status_code, headers={
                        'content-type': 'application/json'})

    return response
