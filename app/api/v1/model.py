
from typing import List
import logging
import os

from fastapi import APIRouter, Depends, File, UploadFile

from app.deps import get_flow
from app.flow import Flow
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/predict")
async def generate_statics(files: List[UploadFile] = File(...), flow: Flow = Depends(get_flow)):
    return await flow.runtime.predict(files)
    