

import logging

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db import models
from app.deps import get_orm_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
def get_settings(
    db: Session = Depends(get_orm_db)
    ):
    return db.query(models.Settings).all()

