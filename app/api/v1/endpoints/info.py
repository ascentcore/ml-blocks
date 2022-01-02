
import logging

from fastapi import APIRouter


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

from app.default.name import get_name

@router.get("/")
def read_root():
    return {"App": get_name()}

@router.get("/status")
async def status():
    return "Status!"