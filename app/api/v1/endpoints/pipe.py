
import logging
from fastapi.param_functions import Depends

from app.db import models
from app.api import deps
from fastapi import APIRouter, Request, Response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.put("/register")
async def register(request: Request, runtime = Depends(deps.get_runtime), db = Depends(deps.get_orm_db)):
    logger.info(f'Registering host {request.client.host}')
    runtime.register(request.client.host, db)

@router.get('/graph')
def get_graph(runtime = Depends(deps.get_runtime), db = Depends(deps.get_orm_db)):
    children =  db.query(models.Dependency).all()
    graph = runtime.get_graph(children)
    return graph

@router.get('/deps')
def get_graph(db = Depends(deps.get_orm_db)):
    return db.query(models.Dependency).all()

@router.get('/root')
def get_root(runtime = Depends(deps.get_runtime)):
    return runtime.get_root()