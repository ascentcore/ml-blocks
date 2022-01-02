
import logging

from fastapi import APIRouter, Depends
from app.store import Storage
from app.api import deps
from app.runtime import runtime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()



@router.get("/")
def train(db: Storage = Depends(deps.get_db)):
    data = db.load()
    runtime.train(data)
