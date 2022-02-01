import logging
from fastapi import APIRouter, Depends, Request

from app.registry import Registry
from app.db import models

from app.deps import get_registry, get_orm_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.put("/register")
def register(
    request: Request,
    db = Depends(get_orm_db),
    registry: Registry = Depends(get_registry)
):
    registry.register(db, request.client.host)

@router.get("/dependencies")
def register(db = Depends(get_orm_db)):
     return db.query(models.Dependency).all()