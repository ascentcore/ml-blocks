
from typing import List

import logging
import os


from fastapi import APIRouter
from app.process import Process
from app.loaders.loader_factory import get_loader


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
def get_data():
    return os.walk('/app/generated')
