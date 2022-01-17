
from typing import List

import logging


from fastapi import APIRouter, Depends, File, UploadFile, Form
from app.store import Storage

from app import deps
from app.runtime import runtime
from app.process import Process
from app.loaders.loader_factory import get_loader


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/")
def get_data(db: Storage = Depends(deps.get_db)):
    return db.load()

@router.get("/refresh")
def refresh(
        pipeline = Depends(deps.get_piepline), 
        runtime=Depends(deps.get_runtime),
        db: Storage = Depends(deps.get_db)):
    if pipeline.dependency != None:
        process = Process(runtime, pipeline, db)
        process.refresh()


@router.post("/uploadfiles")
def create_upload_file(
        runtime=Depends(deps.get_runtime), 
        pipeline = Depends(deps.get_piepline), 
        files: List[UploadFile] = File(...),
        db = Depends(deps.get_orm_db),
        loader: str = Form('csv'),
        append: bool = Form(None)):
    
    loader = get_loader(loader)
    loader.load_files(files)
    process = Process(runtime, pipeline, db)
    process.upload(loader, append)
