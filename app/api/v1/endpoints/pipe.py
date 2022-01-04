
import logging
from app import deps
from fastapi.param_functions import Depends

from app.db import models

from fastapi import APIRouter, Request, Response

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.put("/register")
async def register(request: Request, pipeline = Depends(deps.get_piepline), db = Depends(deps.get_orm_db)):
    logger.info(f'Registering host {request.client.host}')
    pipeline.register(request.client.host, db)

@router.get('/graph')
def get_graph(
        runtime = Depends(deps.get_runtime),
        pipeline = Depends(deps.get_piepline), 
        db = Depends(deps.get_orm_db)):  
    return pipeline.get_graph(runtime, db)

@router.get('/deps')
def get_graph(db = Depends(deps.get_orm_db)):
    return db.query(models.Dependency).all()

@router.get('/root')
def get_root(runtime = Depends(deps.get_runtime)):
    return runtime.get_root()